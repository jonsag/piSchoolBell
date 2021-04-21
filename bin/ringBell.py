#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import getopt, sys

from datetime import datetime
from time import sleep

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print ("Error importing RPi.GPIO!")

from modules import (
    db_connect,
    db_create_cursor,
    db_close_cursor,
    db_disconnect,
    db_query,
    bellRelayGpio,
    onError,
)

try:
    myopts, args = getopt.getopt(
        sys.argv[1:], "d:" "t:" "vh", ["date=", "time=", "verbose", "help"]
    )

except getopt.GetoptError as e:
    onError(1, str(e))

# if len(sys.argv) == 1:  # no options passed
#    onError(2, 2)

dateNow = ""
timeNow = ""
verbose = False

for option, argument in myopts:
    if option in ("-d", "--date"):
        dateNow = argument
    if option in ("-t", "--time"):
        timeNow = argument
    elif option in ("-v", "--verbose"):  # verbose output
        verbose = True

# get current time
dateTimeNow = datetime.now()
if not dateNow:
    dateNow = str(dateTimeNow.strftime("%Y-%m-%d"))

if not timeNow:
    timeNow = dateTimeNow.strftime("%H:%M")

weekNumberNow = datetime.strptime(dateNow, "%Y-%m-%d").strftime("%W")

dayNumberNow = int(datetime.strptime(dateNow, "%Y-%m-%d").strftime("%w")) - 1
if dayNumberNow == -1:
    dayNumberNow = 6

if verbose:
    print("*** Date: %s \n    Time: %s \n    Week number: %s \n    Day number: %s" % (
        dateNow,
        timeNow,
        weekNumberNow,
        dayNumberNow,
    ))

# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx, verbose)

# check if day is school day
isSchoolDay = False
if verbose:
    print("\n*** Checking if today is a school day...")
query = "SELECT * FROM days WHERE " "date = '" + dateNow + "' AND " "isWorkDay = '1'"
result, rowCount = db_query(cursor, query, verbose)  # run query
if rowCount:  # result found, is a work day
    isSchoolDay = True
    if verbose:
        print "*** This is a school day"

# check if day is not on a break
isNotOnBreak = False
if isSchoolDay:
    if verbose:
        print "\n*** Checking if today is not on a break..."
    query = (
        "SELECT * FROM breaks WHERE "
        "startDate <= '" + dateNow + "' AND "
        "endDate >= '" + dateNow + "'"
    )
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if not rowCount:  # nothing found, not on a break
        isNotOnBreak = True
        if verbose:
            print "*** This is not on a break"
else:  # check if today is an extra school day
    if verbose:
        print "\n*** Checking if today is an extra school day..."
    query = "SELECT * FROM extraDays WHERE " "extraDayDate = '" + dateNow + "'"
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:
        isNotOnBreak = True
        if verbose:
            print "*** This is an extra school day"


# check if it is time to ring bell and what ring pattern to use
isRingTime = False
if isNotOnBreak:
    if verbose:
        print "\n*** Checking if it is time to ring the bell..."
    query = (
        "SELECT weekDays, ringPatternId FROM ringTimes WHERE "
        "ringTime = '" + timeNow + "'"
    )
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:
        if verbose:
            print "*** It is time to ring bell"
        for row in result:
            weekDays = row[0]
            ringPatternId = row[1]
        if weekDays[dayNumberNow] == "1":
            isRingTime = True
            if verbose:
                print "*** This ring time is valid today"

# find ring pattern
ringPattern = ""
if isRingTime:
    if verbose:
        print "\n*** Looking up which ring pattern to use..."
    query = (
        "SELECT ringPattern FROM ringPatterns WHERE "
        "ringPatternId = '" + str(ringPatternId) + "'"
    )
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:
        for row in result:
            ringPattern = row[0]

# ring pattern
bellRelayState = False
if ringPattern != "":
    # set up gpio
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(bellRelayGpio, GPIO.OUT, initial=GPIO.LOW)

    ringPattern = ringPattern.replace(" ", "").split(",")  # shape ring pattern

    i = 0
    if verbose:
        print

    for time in ringPattern:
        timeDelay = (
            float(int(ringPattern[i])) / 10
        )  # delay is stated in tenth of a second
        if i % 2 == 0:
            if verbose:
                print "*** Ringing bell for %s s..." % timeDelay
            bellRelayState = True
        else:
            if verbose:
                print "*** Pausing bell for %s s..." % timeDelay
            bellRelayState = False

        GPIO.output(bellRelayGpio, bellRelayState)  # set bell gpio pin
        sleep(timeDelay)  # ring or pause

        i += 1

    GPIO.output(bellRelayGpio, False)  # make sure relay is turned off
    if verbose:
        print "*** Stopped ringing"

    GPIO.cleanup(bellRelayGpio)

# close cursor
db_close_cursor(cnx, cursor, verbose)

# close db
db_disconnect(cnx, verbose)
