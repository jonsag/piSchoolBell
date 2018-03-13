#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

from datetime import datetime, timedelta

from modules import (htmlFormEscape, dayName, 
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
    print '<br>\n'
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
    
def isRingDay(date, weekNumber, verbose):
    isWorkDay = False
    isNotOnBreak = False
    
    dayNumber = -1
    breakName = ''
    
    query = ("SELECT date, weekNumber, dayNumber FROM days WHERE "
             "date = '" + date + "' "
             "AND "
             "isWorkDay = '1' "
             )
    if verbose:
        print "<br>\n"
        print "<br>\n*** Running query: \n    %s" % query
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if verbose:
        print "<br>\n*** Row count: %s" % rowCount
    if rowCount:
        isWorkDay = True
        if verbose:
            print "<br>\n*** This is a school day"
        for row in result:
            ringDate = row[0] # this is the day we are going to look for
            weekNumber = row[1]
            dayNumber = row[2]
            if verbose:
                print "<br>\n*** Date: %s" % ringDate
                print "<br>\n--- Week number: %s" % weekNumber
                print "<br>\n--- Day number: %s" % dayNumber

            
    # check if this is on a break
    if isWorkDay:
        query = ("SELECT breakName FROM breaks WHERE " 
                 "startDate <= '" + str(ringDate) + "' AND "
                 "endDate >= '" + str(ringDate) + "'"
                 )
        if verbose:
            print "<br>\n*** Running query: \n    %s" % query
        result, rowCount = db_query(cursor, query, verbose)  # run query
        if verbose:
            print "<br>\n*** Row count: %s" % rowCount
        if not rowCount: # nothing found, not on a break
            isNotOnBreak = True
            if verbose:
                print "<br>\n*** This is not on a break"
        else:
            for row in result:
                breakName = row[0]
                if verbose:
                    print "<br>\n*** Break name: %s" % breakName
    
    return isWorkDay, isNotOnBreak, weekNumber, dayNumber, breakName 

def findRingTimes(date, dayNumber, verbose):
    foundRingTime = False
    
    ringTimes = []
    
    # find ring times
    if verbose:
        print "<br>\n*** Checking if it is time to ring the bell..."
    query = ("SELECT ringTimeName, weekDays, TIME_FORMAT(ringTime, '%H:%i') as ringTime, ringPatternId FROM ringTimes "
             "ORDER BY ringTime ASC" 
             )
    if verbose:
        print "*** Running query: \n    %s" % query
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:
        if verbose:
            print "<br>\n*** It is time to ring bell"
        for row in result:
            ringTimeName = row[0]
            weekDays = row[1]
            ringTime = row[2]
            ringPatternId = row[3]
            if str(weekDays)[dayNumber] == "1":
                
                if verbose:
                    print "<br>\n*** This ring time is valid today"
                    print "<br>\n*** Ring time name: %s" % ringTimeName
                    print "<br>\n*** Week days: %s" % weekDays
                    print "<br>\n*** Ring time: %s" % ringTime
                    print "<br>\n*** Ring pattern id: %s" % ringPatternId
                    
                # find ring pattern
                query = ("SELECT ringPatternName, ringPattern FROM ringPatterns WHERE " 
                 "ringPatternId = '" + str(ringPatternId) + "'"
                 )
                if verbose:
                    print "<br>\n*** Running query: \n    %s" % query
                result, rowCount = db_query(cursor, query, verbose)  # run query
                if rowCount:
                    for row in result:
                        ringPatternName = row[0]
                        ringPattern = row[1]
                        
                    ringTimes.append({'ringTimeName': ringTimeName,
                                      'ringTime': ringTime,
                                      'ringPatternName': ringPatternName, 
                                      'ringPattern': ringPattern
                                      })
                    
    return ringTimes

def pageBody():    

    date = dateNow
    
    oldWeekNumber = 0
    
    i = 0
    
    while True:
        isWorkDay, isNotOnBreak, weekNumber, dayNumber, breakName = isRingDay(date, oldWeekNumber, verbose)
        
        if weekNumber != oldWeekNumber:
            print "<br><br>\nWeek number: %s" % weekNumber
            oldWeekNumber = weekNumber
                    
        if isNotOnBreak or isWorkDay:
            print "<br>\n&nbsp;&nbsp;&nbsp;&nbsp;%s, %s" % (date, dayName(dayNumber, verbose))

        if breakName:
            print "<br>\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s" % breakName
            
        if isNotOnBreak:
            ringTimes = findRingTimes(date, dayNumber, verbose)
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