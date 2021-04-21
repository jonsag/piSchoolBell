#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi
import cgitb

cgitb.enable()  # for troubleshooting

from datetime import datetime

from modules import (
    nextRing,
    webPageFooter,
    webPageHeader,
    db_connect,
    db_create_cursor,
    db_close_cursor,
    db_disconnect,
    db_query,
)

verbose = False

print "Content-type: text/html"
print

print """
<html>

<head><title>piSchoolBell</title></head>
 
<body>
 
<h3> piSchoolBell </h3>
"""

# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx, verbose)

# get current time
dateTimeNow = datetime.now()

dateNow = dateTimeNow.strftime("%Y-%m-%d")

timeNow = dateTimeNow.strftime("%H:%M")


def pageLinks():

    print '\n<br><a href="upcomingRings.py">Upcoming rings</a>'

    print "\n<br>"

    print "\n<br>"
    print '\n<br><a href="ringTimes.py">Ring times</a>'

    print "\n<br>"
    print '\n<br><a href="schoolBreaks.py">Breaks</a>'

    # print '\n<br>'
    # print '\n<br><a href="extraDays.py">Extra school days</a>'

    print "\n<br>"
    print '\n<br><a href="ringPatterns.py">Ring patterns</a>'

    print "\n<br>"

    print "\n<br>"
    print '\n<br><a href="status.py">Status</a>'


def pageFooter():
    webPageFooter


def pageBody():

    # find next time for ring
    (
        nextRingDay,
        nextRingDate,
        nextRingTime,
        ringTimeName,
        ringPatternName,
        ringPattern,
    ) = nextRing(cursor, dateNow, timeNow, verbose)

    print "\n<br>%s \n<br>%s" % (dateNow, timeNow)

    print "\n<br>"

    print "\n<br>Next ring:"
    print ("\n<br>&nbsp;&nbsp;&nbsp;&nbsp%s, %s" % (nextRingDate, nextRingDay))
    print (
        "\n<br>&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp%s, %s"
        % (nextRingTime, ringTimeName)
    )
    print (
        "\n<br>&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp%s, %s"
        % (ringPatternName, ringPattern)
    )

    print "\n<br>"


if __name__ == "__main__":
    webPageHeader()
    pageBody()
    pageLinks()
    webPageFooter()


# close cursor
db_close_cursor(cnx, cursor, verbose)

# close db
db_disconnect(cnx, verbose)

print """
 

 
</body>

</html>
"""