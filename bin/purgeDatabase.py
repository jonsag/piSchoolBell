#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from modules import (
    db_connect,
    db_create_cursor,
    db_close_cursor,
    db_disconnect,
    db_query,
    onError,
    logFile,
    writeToFile,
)

import getopt, sys, MySQLdb

from datetime import date
from dateutil.relativedelta import relativedelta
from urlparse import urljoin
from urllib2 import urlopen

try:
    myopts, args = getopt.getopt(
        sys.argv[1:], "pc" "vh", ["pretend", "cron", "verbose", "help"]
    )

except getopt.GetoptError as e:
    onError(1, str(e))

if len(sys.argv) == 1:  # no options passed
    onError(2, 2)

logging = False
purge = False
verbose = False

for option, argument in myopts:
    if option in ("-p", "--purge"):
        purge = True
    if option in ("-c", "--cron"):
        logging = True
        purge = True
    elif option in ("-v", "--verbose"):
        verbose = True

timeNow = date.today()
dateNow = timeNow.strftime("%Y-%m-%d")

if logging:
    writeToFile(logFile, "Purge database: Started", verbose)

# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx, verbose)

# delete from dates
if verbose:
    print "\n*** Finding dates older than today..."
query = "SELECT dayId, date FROM days WHERE " "date < '" + dateNow + "'"
result, rowCount = db_query(cursor, query, verbose)  # run query
if rowCount:  # result found, is a work day
    if purge and verbose:
        print "\n*** The following dates will be deleted:"
    elif verbose:
        print "\n*** The following dates is up for deletion:"
    for row in result:
        if verbose:
            print "    Id %s: %s" % (row[0], row[1])

    query = "DELETE FROM days WHERE " "date < '" + dateNow + "'"
    if purge:
        result, rowCount = db_query(cursor, query, verbose)  # run query
        if rowCount:  # result found, is a work day
            if verbose:
                print "*** %s dates deleted" % rowCount
            if logging:
                writeToFile(
                    logFile, "Purge database: %s days deleted" % rowCount, verbose
                )
else:
    if verbose:
        print "*** No obsolete dates found"


# delete from breaks
if verbose:
    print "\n*** Finding dates older than today..."
query = (
    "SELECT breakId, breakName, startDate, endDate FROM breaks WHERE "
    "endDate < '" + dateNow + "'"
)
result, rowCount = db_query(cursor, query, verbose)  # run query
if rowCount:  # result found, is a work day
    if purge and verbose:
        print "\n*** The following breaks will be deleted:"
    elif verbose:
        print "\n*** The following breaks is up for deletion:"
    for row in result:
        if verbose:
            print "    Id %s: %s, %s, %s" % (row[0], row[1], row[2], row[3])

    query = "DELETE FROM breaks WHERE " "endDate < '" + dateNow + "'"
    if purge:
        result, rowCount = db_query(cursor, query, verbose)  # run query
        if rowCount:  # result found, is a work day
            if verbose:
                print "*** %s breaks deleted" % rowCount
            if logging:
                writeToFile(
                    logFile, "Purge database: %s breaks deleted" % rowCount, verbose
                )
else:
    if verbose:
        print "*** No obsolete breaks found"

# delete from extraDays
if verbose:
    print "\n*** Finding extra days older than today..."
query = (
    "SELECT extraDayId, extraDayName, extraDayDate FROM extraDays WHERE "
    "extraDayDate < '" + dateNow + "'"
)
result, rowCount = db_query(cursor, query, verbose)  # run query
if rowCount:  # result found, is a work day
    if purge and verbose:
        print "\n*** The following breaks will be deleted:"
    elif verbose:
        print "\n*** The following breaks is up for deletion:"
    for row in result:
        if verbose:
            print "    Id %s: %s, %s, %s" % (row[0], row[1], row[2], row[3])

    query = "DELETE FROM extraDays WHERE " "extraDayDate < '" + dateNow + "'"
    if purge:
        result, rowCount = db_query(cursor, query, verbose)  # run query
        if rowCount:  # result found, is a work day
            if verbose:
                print "*** %s extra days deleted" % rowCount
            if logging:
                writeToFile(
                    logFile, "Purge database: %s extra days deleted" % rowCount, verbose
                )
else:
    if verbose:
        print "*** No obsolete extra days found"

# close cursor
db_close_cursor(cnx, cursor, verbose)

# close db
db_disconnect(cnx, verbose)

if logging:
    writeToFile(logFile, "Purge database: Ended", verbose)