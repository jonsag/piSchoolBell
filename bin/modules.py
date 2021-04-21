#!/usr/bin/env pythone
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import os, sys, MySQLdb, time, urllib2, socket

import Adafruit_CharLCD as LCD

from ConfigParser import ConfigParser
from datetime import datetime, timedelta

config = ConfigParser()  # define config file
config.read(
    "%s/config.ini" % os.path.dirname(os.path.realpath(__file__))
)  # read config file

bellRelayGpio = int(config.get("gpioAssignment", "bellRelayGpio").strip(" "))
button1Gpio = config.get("gpioAssignment", "button1Gpio").strip(" ")
button2Gpio = config.get("gpioAssignment", "button2Gpio").strip(" ")
minUptime = int(config.get("misc", "minUptime").strip(" "))

logFile = config.get("paths", "logFile").strip(" ")
gpioWatchLog = config.get("paths", "gpioWatchLog").strip(" ")
tempDir = config.get("paths", "tempDir").strip(" ")

USBDir = config.get("paths", "USBDir").strip(" ")
labelMatch = config.get("paths", "labelMatch").strip(" ").upper()

ipWaitTime = int(config.get("misc", "ipWaitTime").strip(" "))

testAddress = config.get("misc", "testAddress").strip(" ")

unicode_degree_sign = config.get("misc", "unicode_degree_sign").strip(" ")

drygUri = config.get("dryg", "drygUri").strip(" ")
drygPath = config.get("dryg", "drygPath").strip(" ")


def onError(errorCode, extra):
    print "\nError %s" % errorCode
    if errorCode in (1, 12):
        print extra
        usage(errorCode)
    elif errorCode == 2:
        print "No options given"
        usage(errorCode)
    elif errorCode in (3, 4, 5, 8):  # stops execution
        print extra
        sys.exit(errorCode)
    elif errorCode in (6, 7):  # returns to script
        print extra
        return


def usage(exitCode):
    print "\nUsage:"
    print "***************************************-"
    print "%s -1 <text line 1> -2 <text line 2>" % sys.argv[0]
    print "\nMisc options:"
    print "-v    verbose output"
    print "-h    prints this"

    sys.exit(exitCode)


def db_connect(verbose):
    if verbose:
        print "\n*** Connecting to db..."
    dbconfig = ConfigParser()
    dbconfig.read("/home/pi/bin/piSchoolBell/mysql-config.ini")

    servername = dbconfig.get("db", "server")
    username = dbconfig.get("db", "user")
    password = dbconfig.get("db", "password")
    dbname = dbconfig.get("db", "database")

    cnx = MySQLdb.connect(
        host=servername, user=username, passwd=password, db=dbname, charset="utf8"
    )
    # cnx.autocommit(True)

    return cnx


def db_create_cursor(cnx, verbose):
    if verbose:
        print "\n*** Creating cursor..."

    cursor = cnx.cursor()

    return cursor


def db_close_cursor(cnx, cursor, verbose):
    if verbose:
        print "\n*** Closing db cursor..."
    cursor.close()
    if verbose:
        print "    Committing db changes..."
    cnx.commit()


def db_disconnect(cnx, verbose):
    if verbose:
        print "\n*** Disconnecting from db..."
    cnx.close()


def db_query(cursor, query, verbose):
    if verbose:
        print "\n*** Running query: \n    %s" % query
    cursor.execute(query)
    results = cursor.fetchall()

    return results, cursor.rowcount


def db_update(cursor, query, verbose):
    cursor.execute(query)
    results = cursor.fetchall()

    return results


def htmlFormEscape(text):
    # unicode
    html_escape_table = {
        "%E5": u"\00E5",  # å
        "%E4": u"\00E4",  # ä
        "%F6": u"\00F6",  # ö
        "%C5": u"\00C5",  # Å
        "%C4": u"\00C4",  # Å
        "%D6": u"\00D6",  # Ö
    }

    # normal
    # html_escape_table = {"%E5": "å",
    #                     "%E4": "ä",
    #                     "%F6": "ö",
    #                     "%C5": "Å",
    #                     "%C4": "Ä",
    #                     "%D6": "Ö",
    #                     }

    # ascii
    # html_escape_table = {"%E5": "134",
    #                     "%E4": "132",
    #                     "%F6": "148",
    #                     "%C5": "143",
    #                     "%C4": "142",
    #                     "%D6": "153",
    #                     }

    return "".join(html_escape_table.get(c, c) for c in text)


def nextRing(cursor, dateNow, timeNow, verbose):
    isWorkDay = False
    isNotOnBreak = False
    foundRingTime = False

    while True:
        # find first work day
        query = (
            "SELECT date, dayNumber FROM days WHERE "
            "date >= '" + dateNow + "' "
            "AND "
            "isWorkDay = '1' "
            "LIMIT 1"
        )
        result, rowCount = db_query(cursor, query, verbose)  # run query
        if rowCount:
            isWorkDay = True
            if verbose:
                print "*** This is a school day"
            for row in result:
                nextRingDate = row[0]  # this is the day we are going to look for
                dayNumber = row[1]

        # check if this is on a break
        if isWorkDay:
            query = (
                "SELECT * FROM breaks WHERE "
                "startDate <= '" + str(nextRingDate) + "' AND "
                "endDate >= '" + str(nextRingDate) + "'"
            )
            result, rowCount = db_query(cursor, query, verbose)  # run query
            if not rowCount:  # nothing found, not on a break
                isNotOnBreak = True
                if verbose:
                    print "*** This is not on a break"

        # find ring time
        if isNotOnBreak:
            if verbose:
                print "\n*** Checking if it is time to ring the bell..."
            query = (
                "SELECT ringTimeName, weekDays, TIME_FORMAT(ringTime, '%H:%i') as ringTime, ringPatternId "
                "FROM ringTimes WHERE "
                "ringTime >= '" + timeNow + "' "
                "LIMIT 1"
            )
            result, rowCount = db_query(cursor, query, verbose)  # run query
            if rowCount:
                if verbose:
                    print "*** It is time to ring bell"
                for row in result:
                    ringTimeName = row[0]
                    weekDays = row[1]
                    nextRingTime = row[2]
                    ringPatternId = row[3]
                if weekDays[dayNumber] == "1":
                    foundRingTime = True
                    if verbose:
                        print "*** This ring time is valid today"

        if foundRingTime:
            break
        else:
            dateNow = datetime.strptime(dateNow, "%Y-%m-%d")  # convert to time object
            dateNow = dateNow + timedelta(days=1)  # add one day
            dateNow = datetime.strftime(dateNow, "%Y-%m-%d")  # convert to string

            timeNow = "00:00"  # set time to midnight on the parsed date

    # find ring pattern
    query = (
        "SELECT ringPatternName, ringPattern FROM ringPatterns WHERE "
        "ringPatternId = '" + str(ringPatternId) + "'"
    )
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:
        for row in result:
            ringPatternName = row[0]
            ringPattern = row[1]

    nextRingDay = getDayName(dayNumber, verbose)

    return (
        nextRingDay,
        nextRingDate,
        nextRingTime,
        ringTimeName,
        ringPatternName,
        ringPattern,
    )


def validateDate(date, verbose):
    dateValid = True

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        dateValid = False
        if verbose:
            print "*** Incorrect data format, should be YYYY-MM-DD"

    return dateValid


def validateTime(time, verbose):
    timeValid = True

    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        timeValid = False
        if verbose:
            print "*** Incorrect time format, should be hh:mm"

    return timeValid


def webPageHeader():
    print "<hr>"


def webPageFooter():
    for i in range(0, 5):
        print "<br>\n"

    print "<br>\n<hr>"
    print "<br>\n&copy; Jonix 2018"
    print (
        '<br>\n<a href="mailto:jonsagebrand@gmail.com?subject=piShoolBell@%s">jonsagebrand@gmail.com</a>'
        % socket.gethostname()
    )

    for i in range(0, 5):
        print "<br>\n"


def countEntriesInDatabase(tableName, cursor, verbose):
    query = "SELECT COUNT(*) FROM " + tableName
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:
        for row in result:
            count = row[0]

    return count


def tableLastUpdated(tableName, cursor, verbose):
    answer = ""
    query = "SHOW TABLE STATUS FROM piSchoolBell LIKE '" + tableName + "'"
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:
        for row in result:
            answer = row[11]

    return answer


def isRingDay(date, weekNumber, cursor, verbose):
    isWorkDay = False
    isNotOnBreak = False

    dayNumber = -1
    breakName = ""

    query = (
        "SELECT date, weekNumber, dayNumber FROM days WHERE "
        "date = '" + date + "' "
        "AND "
        "isWorkDay = '1' "
    )
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if verbose:
        print "<br>\n*** Row count: %s" % rowCount
    if rowCount:
        isWorkDay = True
        if verbose:
            print "<br>\n*** This is a school day"
        for row in result:
            ringDate = row[0]  # this is the day we are going to look for
            weekNumber = row[1]
            dayNumber = row[2]
            if verbose:
                print "<br>\n*** Date: %s" % ringDate
                print "<br>\n*** Week number: %s" % weekNumber
                print "<br>\n*** Day number: %s" % dayNumber

    # check if this is on a break
    if isWorkDay:
        query = (
            "SELECT breakName FROM breaks WHERE "
            "startDate <= '" + str(ringDate) + "' AND "
            "endDate >= '" + str(ringDate) + "'"
        )
        result, rowCount = db_query(cursor, query, verbose)  # run query
        if verbose:
            print "<br>\n*** Row count: %s" % rowCount
        if not rowCount:  # nothing found, not on a break
            isNotOnBreak = True
            if verbose:
                print "<br>\n*** This is not on a break"
        else:
            for row in result:
                breakName = row[0]
                if verbose:
                    print "<br>\n*** Break name: %s" % breakName

    return isWorkDay, isNotOnBreak, weekNumber, dayNumber, breakName


def findRingTimes(date, dayNumber, cursor, verbose):
    foundRingTime = False

    ringTimes = []

    # find ring times
    if verbose:
        print "<br>\n*** Checking if it is time to ring the bell..."
    query = (
        "SELECT ringTimeName, weekDays, TIME_FORMAT(ringTime, '%H:%i') as ringTime, ringPatternId FROM ringTimes "
        "ORDER BY ringTime ASC"
    )
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:
        if verbose:
            print "<br>\n*** It is time to ring bell"
        for row in result:
            ringTimeName = row[0]
            weekDays = row[1]
            ringTime = row[2]
            ringPatternId = row[3]
            if weekDays[dayNumber] == "1":

                if verbose:
                    print "<br>\n*** This ring time is valid today"
                    print "<br>\n*** Ring time name: %s" % ringTimeName
                    print "<br>\n*** Week days: %s" % weekDays
                    print "<br>\n*** Ring time: %s" % ringTime
                    print "<br>\n*** Ring pattern id: %s" % ringPatternId

                # find ring pattern
                query = (
                    "SELECT ringPatternName, ringPattern FROM ringPatterns WHERE "
                    "ringPatternId = '" + str(ringPatternId) + "'"
                )
                result, rowCount = db_query(cursor, query, verbose)  # run query
                if rowCount:
                    for row in result:
                        ringPatternName = row[0]
                        ringPattern = row[1]

                    ringTimes.append(
                        {
                            "ringTimeName": ringTimeName,
                            "ringTime": ringTime,
                            "ringPatternName": ringPatternName,
                            "ringPattern": ringPattern,
                        }
                    )

    return ringTimes


def getUptime():
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds


def internetAccess(testAddress, verbose):
    connected = False

    if verbose:
        print "*** Looking up %s" % testAddress

    try:
        urllib2.urlopen("http://%s" % testAddress, timeout=1)
    except urllib2.URLError as err:
        if verbose:
            print "*** Error: \n    %s" % err
    else:
        connected = True

    if verbose and connected:
        print "*** We are connected to internet"

    return connected


def getDayName(dayNumber, verbose):
    dayName = "Wrong day number"

    if verbose:
        print "*** Getting day name from day number %s" % dayNumber

    if isinstance(dayNumber, basestring):
        dayName = int(dayNumber)

    if dayNumber == 0:
        dayName = "Monday"
    elif dayNumber == 1:
        dayName = "Tuesday"
    elif dayNumber == 2:
        dayName = "Wednesday"
    elif dayNumber == 3:
        dayName = "Thursday"
    elif dayNumber == 4:
        dayName = "Friday"
    elif dayNumber == 5:
        dayName = "Saturday"
    elif dayNumber == 6:
        dayName = "Sunday"

    return dayName


def writeToFile(logFile, message, verbose):
    timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    message = "%s: %s" % (timeStamp, message)

    if verbose:
        print "\n*** Writing to %s" % logFile
        print "    %s" % message

    with open(logFile, "a") as f:
        f.write("{}\n".format(message))


def splitPath(path, verbose):
    if verbose:
        print "\n*** Extracting directory, file name and extension from\n    %s ..." % path

    dirName = os.path.dirname(path)

    f = os.path.basename(path)
    fileName = os.path.splitext(f)[0]
    extension = os.path.splitext(f)[1].strip(".")

    if verbose:
        print "    Directory: %s" % dirName
        print "    File name: %s" % fileName
        print "    Extension: %s" % extension

    return dirName, fileName, extension


def tableSelection(table, verbose):
    selection = ""

    if table == "days":
        selection = "dayId, date, dayName, weekNumber, dayNumber, isWorkDay"
    elif table == "breaks":
        selection = "breakId, breakName, startDate, endDate"
    elif table == "ringTimes":
        selection = "ringTimeId, ringTimeName, weekDays, ringTime, ringPatternId"
    elif table == "ringPatterns":
        selection = "ringPatternId, ringPatternName, ringPattern"

    return selection


def findUSBMountPoint(USBDir, labelMatch, verbose):
    foundDirs = []

    if verbose:
        print "\n*** Searching for USB mounted at %s \n    with label matching '%s' ..." % (
            USBDir,
            labelMatch,
        )

    for d in os.listdir(USBDir):
        path = os.path.join(USBDir, d)
        if d.startswith(labelMatch) and os.path.isdir(path):
            foundDirs.append(path)

    if foundDirs:
        if verbose:
            if verbose:
                print "*** Found USB: %s" % foundDirs[0]
        return foundDirs[0]
    else:
        if verbose:
            print "*** Did not find any USB"
        return ""


def initialize_lcd(verbose):
    if verbose:
        print "\n*** Initializing LCD..."

    # read config for LCD
    lcd_rs = int(config.get("lcd", "lcd_rs").strip(" "))
    lcd_en = int(config.get("lcd", "lcd_en").strip(" "))
    lcd_d4 = int(config.get("lcd", "lcd_d4").strip(" "))
    lcd_d5 = int(config.get("lcd", "lcd_d5").strip(" "))
    lcd_d6 = int(config.get("lcd", "lcd_d6").strip(" "))
    lcd_d7 = int(config.get("lcd", "lcd_d7").strip(" "))
    lcd_backlight = int(config.get("lcd", "lcd_backlight").strip(" "))

    lcd_columns = int(config.get("lcd", "lcd_columns").strip(" "))
    lcd_rows = int(config.get("lcd", "lcd_rows").strip(" "))

    lcd_wake_time = int(config.get("lcd", "lcd_wake_time").strip(" "))

    # Initialize the LCD using the pins from config
    lcd = LCD.Adafruit_CharLCD(
        lcd_rs,
        lcd_en,
        lcd_d4,
        lcd_d5,
        lcd_d6,
        lcd_d7,
        lcd_columns,
        lcd_rows,
        lcd_backlight,
    )

    return lcd, lcd_wake_time, lcd_columns


def remove_leading_zero(string):
    if len(string) == 2:
        string = string.lstrip("0")

    return string


def degree_sign(lcd, cursor, row):
    # degree symbol
    lcd.create_char(
        1, [0b01100, 0b10010, 0b10010, 0b01100, 0b00000, 0b00000, 0b00000, 0b00000]
    )

    lcd.set_cursor(cursor, row)

    lcd.message("\x01")

    return lcd


def hourglass_symbol(lcd, cursor, row):
    # hourglass
    lcd.create_char(
        2, [0b11111, 0b10001, 0b01110, 0b00100, 0b01010, 0b10001, 0b11111, 0b00000]
    )

    lcd.set_cursor(cursor, row)

    lcd.message("\x02")

    return lcd


def infinity_symbol(lcd, cursor, row):
    # infinity
    lcd.create_char(
        3, [0b00000, 0b00000, 0b01010, 0b10101, 0b10101, 0b01010, 0b00000, 0b00000]
    )

    lcd.set_cursor(cursor, row)

    lcd.message("\x03")

    return lcd


def print_to_LCD(lcd, cursor, row, line, message, lcd_columns, verbose):

    t = u"\u00b0"  # degree sign
    inf = u"\u221e"  # infinity symbol

    orig_length = len(message)
    if verbose:
        print "\nLine %s: '%s'" % (line, message)
        print "*** Length: %s" % orig_length
    # else:
    #    print "%s" % (message)

    spaces = lcd_columns - orig_length

    if spaces > 0:
        message = message.ljust(16, " ")
    if verbose:
        print "*** Added %s space(s)" % spaces

    if t in message or inf in message:  # message contains special characters
        message_list = list(message)
        for char in message_list:
            lcd.set_cursor(cursor, row)  # insert text at column and row
            if char == t:
                lcd = degree_sign(lcd, cursor, row)  # print degree sign
            elif char == inf:
                # lcd.message('e')
                lcd = infinity_symbol(lcd, cursor, row)  # print infinity sign
            else:
                lcd.message(char)
            cursor += 1

    else:
        lcd.set_cursor(cursor, row)  # insert text at column and row
        lcd.message(message)

    if len(message) > lcd_columns:
        if verbose:
            print "*** Scrolling"
        for i in range(lcd_columns - orig_length):
            time.sleep(0.5)
            lcd.move_left()


def displayOnLCD(line_1, line_2, verbose):

    # wake up LCD
    lcd, lcd_wake_time, lcd_columns = initialize_lcd(verbose)  # load lcd
    lcd.clear()  # clear screen

    if not line_1:
        # get current time
        dateTimeNow = datetime.now()
        timeNow = dateTimeNow.strftime("%H:%M")
        dateNow = str(dateTimeNow.strftime("%Y-%m-%d"))

        time = dateTimeNow.strftime("%H:%M")
        day = remove_leading_zero(dateTimeNow.strftime("%d"))
        month = remove_leading_zero(dateTimeNow.strftime("%m"))
        year = dateTimeNow.strftime("%Y")
        line_1 = "%s %s/%s %s" % (time, day, month, year)

    if not line_2:
        # connect to database
        cnx = db_connect(verbose)

        # create cursor
        cursor = db_create_cursor(cnx, verbose)

        (
            nextRingDay,
            nextRingDate,
            nextRingTime,
            ringTimeName,
            ringPatternName,
            ringPattern,
        ) = nextRing(cursor, dateNow, timeNow, verbose)
        day = remove_leading_zero(nextRingDate.strftime("%d"))
        month = remove_leading_zero(nextRingDate.strftime("%m"))
        year = nextRingDate.strftime("%Y")
        line_2 = "%s %s/%s %s" % (nextRingTime, day, month, year)

        # close cursor
        db_close_cursor(cnx, cursor, verbose)

        # close db
        db_disconnect(cnx, verbose)

    # print to LCD
    print_to_LCD(lcd, 0, 0, "1", line_1, lcd_columns, verbose)
    print_to_LCD(lcd, 0, 1, "2", line_2, lcd_columns, verbose)
