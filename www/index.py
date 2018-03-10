#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

from datetime import datetime

from modules import (nextRing, 
                     db_connect, db_create_cursor, db_close_cursor, db_disconnect, db_query)

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
cursor = db_create_cursor(cnx)

# get current time
dateTimeNow = datetime.now()

dateNow = dateTimeNow.strftime('%Y-%m-%d')

timeNow = dateTimeNow.strftime('%H:%M')

weekNumberNow = datetime.strptime(dateNow, '%Y-%m-%d').strftime('%W')
    
dayNumberNow = int(datetime.strptime(dateNow, '%Y-%m-%d').strftime('%w')) - 1
if dayNumberNow == -1:
    dayNumberNow = 6
    
def pageBody():
    
    # find next time for ring
    nextRingDay, nextRingDate, nextRingTime, ringTimeName, ringPatternName, ringPattern = nextRing(cursor, dateNow, timeNow, verbose)
    
    print '<br>\nDate: %s <br>\nTime: %s <br>\nWeek number: %s <br>\nDay number: %s' % (dateNow, timeNow, weekNumberNow, dayNumberNow)
    
    print '<br>\n'
    print '<br>\nNext ring: %s <br>\n%s %s, %s' % (ringTimeName.encode('Latin1'), nextRingDay, nextRingDate, nextRingTime)
    print '<br>\n'
    print '<br>\nRing pattern: %s <br>\n %s' % (ringPatternName.encode('Latin1'), ringPattern)
    
    print '<br>\n'
    print '<br>\n<a href="upcomingRings.py">Upcoming rings</a>'
    
    print '<br>\n'
    print '<br>\n<a href="ringTimes.py">Ring times</a>'
    
    print '<br>\n'
    print '<br>\n<a href="breaks.py">Breaks</a>'
    
    print '<br>\n'
    print '<br>\n<a href="extraDays.py">Extra school days</a>'
    
    print '<br>\n'
    print '<br>\n<a href="ringPatterns.py">Ring patterns</a>'


if __name__ == '__main__':
    pageBody()
    
# close cursor
db_close_cursor(cnx, cursor)

# close db
db_disconnect(cnx, verbose)

print """
 

 
</body>

</html>
"""