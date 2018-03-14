#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

from datetime import datetime, timedelta

from modules import (htmlFormEscape, getDayName, findRingTimes, isRingDay, 
                     db_connect, db_create_cursor, db_close_cursor, db_disconnect, db_query)



verbose = False


print "Content-type: text/html"
print

print """
<html>

<head><title>piSchoolBell - upcoming rings</title></head>
 
<body>
 
<h3> piSchoolBell - upcoming rings</h3>
"""


# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx)

# get current time
dateTimeNow = datetime.now()
dateNow = str(dateTimeNow.strftime('%Y-%m-%d'))
timeNow = dateTimeNow.strftime('%H:%M')


def pageLinks():
    print '<br>\n<a href="upcomingRings.py">Reset page</a>'
    
    print '<br>\n'
    print '<br>\n<a href="index.py">Home</a>'
    
    #print '<br>\n'
    #print '<br>\n<a href="upcomingRings.py">Upcoming rings</a>'
    
    print '<br>\n'
    print '<br>\n<a href="ringTimes.py">Ring times</a>'
    
    #print '<br>\n'
    print '<br>\n<a href="schoolBreaks.py">Breaks</a>'
    
    #print '<br>\n'
    #print '<br>\n<a href="extraDays.py">Extra school days</a>'
    
    #print '<br>\n'
    print '<br>\n<a href="ringPatterns.py">Ring patterns</a>'
    
    #print '&emsp;<a href="ringPatterns.py?addRingPattern=1">Add another ring pattern</a>'
    


def pageBody():    

    date = dateNow
    
    oldWeekNumber = 0
    
    i = 0
    
    while True:
        isWorkDay, isNotOnBreak, weekNumber, dayNumber, breakName = isRingDay(date, oldWeekNumber, cursor, verbose)
        
        if weekNumber != oldWeekNumber:
            print "<br><br>\nWeek number: %s" % weekNumber
            oldWeekNumber = weekNumber
                    
        if isNotOnBreak or isWorkDay:
            print "<br>\n&nbsp;&nbsp;&nbsp;&nbsp;%s, %s" % (date, getDayName(dayNumber, verbose))

        if breakName:
            print "<br>\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s" % breakName
            
        if isNotOnBreak:
            ringTimes = findRingTimes(date, dayNumber, cursor, verbose)
            if ringTimes:
                for ringTime in ringTimes:
                    print "<br>\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                    print ("%s, %s" % 
                           (ringTime['ringTime'], 
                            ringTime['ringTimeName'], 
                            ))
                    print "<br>\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                    print ("%s, %s" % 
                           (ringTime['ringPatternName'],
                            ringTime['ringPattern'], 
                            ))
                

        
        i += 1
        if i >= 30:
            break
        else:
            date = datetime.strptime(date, "%Y-%m-%d") # convert to time object
            date = date + timedelta(days=1) # add one day
            date = datetime.strftime(date, "%Y-%m-%d") # convert to string
            
            
if __name__ == '__main__':
    pageLinks()
    pageBody()
    pageLinks()


print """
 

 
</body>

</html>
"""