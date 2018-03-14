#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

print "Content-type: text/html"
print

from datetime import datetime, timedelta

from modules import (nextRing, getUptime, isRingDay, findRingTimes, 
                     db_connect, db_create_cursor, db_close_cursor, db_disconnect, db_query)

verbose = False

print """
<html>

<head><title>piSchoolBell - status</title></head>
 
<body>
 
<h3> piSchoolBell - status</h3>
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
    
    
def countRingTimes(iMax):
    ringCount = 0
    schoolDayCount = 0
    
    date = dateNow
    
    oldWeekNumber = 0
    
    i = 0
    
    while True:
        isWorkDay, isNotOnBreak, weekNumber, dayNumber, breakName = isRingDay(date, oldWeekNumber, cursor, verbose)
        
        #if weekNumber != oldWeekNumber:
        #    oldWeekNumber = weekNumber

        if isNotOnBreak or isWorkDay:
            schoolDayCount += 1
            
        if isNotOnBreak:
            ringTimes = findRingTimes(date, dayNumber, cursor, verbose)
            if ringTimes:
                for ringTime in ringTimes:
                    ringCount += 1
                

        
        i += 1

        if i >= iMax: 
            break
        else:
            date = datetime.strptime(date, "%Y-%m-%d") # convert to time object
            date = date + timedelta(days=1) # add one day
            date = datetime.strftime(date, "%Y-%m-%d") # convert to string
    
    return ringCount, schoolDayCount


def pageLinks():
    print '<br>\n<a href="status.py">Reset page</a>'
    
    print '<br>\n'
    print '<br>\n<a href="index.py">Home</a>'
    
    #print '&emsp;<a href="ringPatterns.py?addRingPattern=1">Add another ring pattern</a>'


def pageBody(): 
    
    print "<br>\n"   

    # time and date
    print ('<br>\nDate: <br>\n&nbsp;&nbsp;&nbsp;&nbsp;%s '
           '<br>\nTime: <br>\n&nbsp;&nbsp;&nbsp;&nbsp;%s '
           '<br>\n<br>\nWeek number: <br>\n&nbsp;&nbsp;&nbsp;&nbsp;%s '
           '<br>\nDay number: <br>\n&nbsp;&nbsp;&nbsp;&nbsp;%s ' 
           % (dateNow, timeNow, weekNumberNow, dayNumberNow)
           )
    
    # uptime
    uptimeSeconds = getUptime()
    uptime = str(timedelta(seconds=uptimeSeconds))
    
    print "<br>\n"  
    print "<br>\nUptime: <br>\n&nbsp;&nbsp;&nbsp;&nbsp;%s" % uptime
    
    ##### database
    print "<br>\n"  
    print "<br>\nDatabase:"
    
    # days
    query = "SELECT COUNT(*) FROM days"
    result, rowCount = db_query(cursor, query, verbose)  # run query
    for row in result:
        dayCount = row[0]
    print "<br>\n&nbsp;&nbsp;&nbsp;&nbspdays entries: %s" % dayCount
    
    # ring times
    query = "SELECT COUNT(*) FROM ringTimes"
    result, rowCount = db_query(cursor, query, verbose)  # run query
    for row in result:
        ringTimeCount = row[0]
    print "<br>\n&nbsp;&nbsp;&nbsp;&nbspringTimes entries: %s" % ringTimeCount
    
    # breaks
    query = "SELECT COUNT(*) FROM breaks"
    result, rowCount = db_query(cursor, query, verbose)  # run query
    for row in result:
        breakCount = row[0]
    print "<br>\n&nbsp;&nbsp;&nbsp;&nbspbreaks entries: %s" % breakCount
    
    # ring patterns
    query = "SELECT COUNT(*) FROM ringPatterns"
    result, rowCount = db_query(cursor, query, verbose)  # run query
    for row in result:
        ringPatternCount = row[0]
    print "<br>\n&nbsp;&nbsp;&nbsp;&nbspringPatterns entries: %s" % ringPatternCount
    
    ## extra days
    #query = "SELECT COUNT(*) FROM extraDays"
    #result, rowCount = db_query(cursor, query, verbose)  # run query
    #for row in result:
    #    extraDayCount = row[0]
    #print "<br>\n&nbsp;&nbsp;&nbsp;&nbspextraDays entries: %s" % extraDayCount
    
    print "<br>\n"
    
    # how long does days run
    query = "SELECT date, DATEDIFF(date,CURDATE())  FROM days ORDER BY date DESC LIMIT 1"
    result, rowCount = db_query(cursor, query, verbose)  # run query
    for row in result:
        lastDate = row[0]
        daysToEnd = row[1]
    print "<br>\n&nbsp;&nbsp;&nbsp;&nbspLast day in database: %s" % lastDate
    
    # last break
    query = "SELECT endDate FROM breaks ORDER BY endDate DESC LIMIT 1"
    result, rowCount = db_query(cursor, query, verbose)  # run query
    for row in result:
        lastBreakEnds = row[0]
    print "<br>\n&nbsp;&nbsp;&nbsp;&nbspLast break ends: %s" % lastBreakEnds
    
    print "<br>\n"
    
    #count rings and school days
    ringCount, schoolDayCount = countRingTimes(daysToEnd)
    print "<br>\n&nbsp;&nbsp;&nbsp;&nbspThere's %s days left in the database" % daysToEnd
    print "<br>\n&nbsp;&nbsp;&nbsp;&nbspOf them %s are school days" % schoolDayCount
    print "<br>\n&nbsp;&nbsp;&nbsp;&nbspBell will ring %s times" % ringCount
    
    
if __name__ == '__main__':
    pageLinks()
    pageBody()
    pageLinks()


print """
 

 
</body>

</html>
"""