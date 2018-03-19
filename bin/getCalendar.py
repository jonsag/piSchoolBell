#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from modules import (db_connect, db_create_cursor, db_close_cursor, db_disconnect, db_query,
                     onError, getDayName, writeToFile, logFile, 
                     drygUri, drygPath)

import getopt, sys, json, MySQLdb

from datetime import date
from dateutil.relativedelta import relativedelta
from urlparse import urljoin
from urllib2 import urlopen

try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 'c'
                                 'vh',
                                 ['cron', 'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))
    
if len(sys.argv) == 1:  # no options passed
    onError(2, 2)
    
addedDays = 0
updatedDays = 0
logging = False
verbose = False
    
for option, argument in myopts:
    if option in ('-c', '--cron'):
        logging = True
    elif option in ('-v', '--verbose'):
        verbose = True
        
        
if logging:
    writeToFile(logFile, "Get calendar: Started", verbose)
        

timeNow = date.today()
dateNow = timeNow.strftime("%Y-%m-%d")
yearNow = timeNow.strftime("%Y")
monthNow = timeNow.strftime("%m")

calendarAddress = urljoin(drygUri, drygPath)

if verbose:
    print "\n*** Todays date: %s" % dateNow
    print
    print "*** Calendar source: %s" % calendarAddress
    
# getting calendars for twelve months
# check if connected to internet
connected = True

if connected:
    # connect to database
    cnx = db_connect(verbose)
    
    # create cursor
    cursor = db_create_cursor(cnx, verbose)
    
    for i in range(0, 12, 1):
        lookupDate = timeNow + relativedelta(months=i)
        lookupYear = lookupDate.strftime("%Y")
        lookupMonth = lookupDate.strftime("%m")
        
        calendarPath = "%s/%s/%s" % (calendarAddress, lookupYear, lookupMonth)
        
        if verbose:
            print "\n*** Getting calendar data for: %s-%s" % (lookupYear, lookupMonth)
            print "    %s" % calendarPath
            
        calendarData = urlopen(calendarPath).read()  # read calendar data
        
        parsedCalendar = json.loads(calendarData)  # load json
        
        if verbose:
            print
            print json.dumps(parsedCalendar, indent=4, sort_keys=True)
            
        cacheTime = parsedCalendar["cachetid"]
        
        day = 0
        
        while True: # will keep on running as long as there is days in a month
                        
            try:  # does this month have this day
                date = parsedCalendar["dagar"][day]["datum"]
            except: # month finished
                break
            
            weekNumber = int(parsedCalendar["dagar"][day]["vecka"])
            dayNumber = int(parsedCalendar["dagar"][day]["dag i vecka"]) - 1
            svDayName = parsedCalendar["dagar"][day]["veckodag"]
            dayName = getDayName(dayNumber, verbose)
            workFreeDay = parsedCalendar["dagar"][day]["arbetsfri dag"]
            
            try:  # is this day an eve
                eve = parsedCalendar["dagar"][day]["helgdagsafton"]
            except:
                eve = ""
            
            try:  # is this day an eve
                holiday = parsedCalendar["dagar"][day]["helgdag"]
            except:
                holiday = ""

            if verbose:
                print "\n*** Date: %s, %s" % (date, dayName)
                if workFreeDay == "Nej":
                    print "    School day"
                if eve:
                    print "    Eve: %s" % eve
                if holiday:
                    print "    Holiday: %s" % holiday
                    
            if workFreeDay == "Nej": # true if this is a school day
                isWorkDay = "1"
            else:
                isWorkDay = "0"
            
            query = ("INSERT INTO days " 
                     "(date, dayName, weekNumber, dayNumber, isWorkDay) " 
                     "VALUES " 
                     "(STR_TO_DATE('" + date + "', '%Y-%m-%d'), "
                     "'" + dayName + "', "
                     "'" + str(weekNumber) + "', "
                     "'" + str(dayNumber) + "', "
                     "'" + isWorkDay + "')")
            try: # insert date in db
                result, rowCount = db_query(cursor, query, verbose) # run query
            except (MySQLdb.IntegrityError) as e: # date already in database
                if verbose:
                    print "*** Date already in table"
                query = ("UPDATE days SET "
                         "dayName = '" + dayName + "', "
                         "weekNumber = '" + str(weekNumber) + "', " 
                         "dayNumber = '" + str(dayNumber) + "', "
                         "isWorkDay = '" + isWorkDay + "' " 
                         "WHERE "
                         "date = '" + date + "'"
                         )
                try: # update item instead
                    result, rowCount = db_query(cursor, query, verbose) # run query
                except MySQLdb.Error as e: # some other error
                    if verbose:
                        print "*** Error: \n    %s" % e
                    sys.exit()
                else:
                    updatedDays = updatedDays + rowCount
            else:
                addedDays = addedDays + rowCount
                                            
            day += 1  # add one day and test it
        
        if verbose:
            print "\n*** Cache time: %s" % cacheTime
            print
            
            if addedDays:
                print "Get calendar: %s days added" % addedDays
            else:
                print "Get calendar: No days added"
                
            if updatedDays:
                print "Get calendar: %s days updated" % updatedDays
            else:
                print "Get calendar: No days updated"
        
    # close cursor
    db_close_cursor(cnx, cursor, verbose)
    
    # close db
    db_disconnect(cnx, verbose)
    
if logging:
    if addedDays:
        writeToFile(logFile, "Get calendar: %s days added" % addedDays, verbose)
    else:
        writeToFile(logFile, "Get calendar: No days added", verbose)
        
    if updatedDays:
        writeToFile(logFile, "Get calendar: %s days updated" % updatedDays, verbose)
    else:
        writeToFile(logFile, "Get calendar: No days updated", verbose)
        
    writeToFile(logFile, "Get calendar: Ended", verbose)





















