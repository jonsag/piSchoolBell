#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi, MySQLdb, re, sys
import cgitb; cgitb.enable()  # for troubleshooting

from calendar import day_name

from modules import (htmlFormEscape, 
                     db_connect, db_create_cursor, db_close_cursor, db_disconnect, db_query)

addRingTime = False # will display form to add ring time

editRingTimeId = "" # this ring time will be edited

newRingTimeName = "" # new time will be inserted
newRingTime = ""

updateRingTimeId = "" # this ring time will be updated
updateRingTimeName = ""
updateRingTime = ""

deleteRingTimeId = "" # this ring time will be deleted

weekDays = list("0000000") # weekDays string

verbose = False

fs = cgi.FieldStorage()

print "Content-type: text/html"
print

print """
<html>

<head><title>piSchoolBell - ring times</title></head>

<style>
table, th, td {
    border: 1px solid black;
}
</style>
 
<body>
 
<h3> piSchoolBell - ring times</h3>
"""

# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx)

for key in fs.keys():
    if key == "deleteRingTimeId": # delete ring time
        deleteRingTimeId = fs[key].value
        
    elif key == "editRingTimeId": # display form to edit ring time
        editRingTimeId = fs[key].value
        
    elif key == "addRingTime" and fs[key].value == "1": # display form to add new ring time
        addRingTime = True
        
    elif key == "newRingTimeName": # add ring time 
        newRingTimeName = fs[key].value
    elif key == "newRingTime":
        newRingTime = fs[key].value
    elif key == "newWeekDays":
        newWeekDays = fs[key].value
    elif key == "newRingPatternId":
        newRingPatternId = fs[key].value
        
    elif key == "updateRingTimeId": # update ring time 
        updateRingTimeId = fs[key].value    
    elif key == "updateRingTimeName": 
        updateRingTimeName = fs[key].value
    elif key == "updateRingTime":
        updateRingTime = fs[key].value
       
    elif key == "Monday": # weekdays 
        weekDays[0] = fs[key].value
    elif key == "Tuesday": 
        weekDays[1] = fs[key].value
    elif key == "Wednesday": 
        weekDays[2] = fs[key].value
    elif key == "Thursday": 
        weekDays[3] = fs[key].value
    elif key == "Friday": 
        weekDays[4] = fs[key].value
    elif key == "Saturday": 
        weekDays[5] = fs[key].value
    elif key == "Sunday": 
        weekDays[6] = fs[key].value

weekDays = ''.join(weekDays)

if deleteRingTimeId: # delete ring time
    query = ("DELETE FROM ringTimes WHERE ringTimeId = '%s'" % deleteRingTimeId)
    try:
        result, rowCount = db_query(cursor, query, verbose)  # run query
    except MySQLdb.Error as e:
        print "<br>\nError: Could not delete time <br>\n%s" % e
        print "<br>\nSQL: %s" % query
    else:
        if rowCount:
            print "\n<br>Deleted ring time with id = %s" % fs[key].value

elif newRingTimeName: # add ring time
    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", newRingTimeName):
        print ("<br>\nError: <br>\nIllegal characters in name!: '" + newRingTimeName + "' "
               "<br>\nNo special characters (including Swedish etc.) allowed "
               "<br>\nOnly characters, digits, spaces and ,. allowed "
               "<br>\nMax 100 characters"
               )
    elif not re.match("^[0-9:]{1,100}$", newRingTime):
        print ("<br>\nError: <br>\nIllegal characters in time!: '" + newRingTime + "' " 
               "<br>\nOnly digits and : allowed "
               )
    else:
        query = ("INSERT INTO ringTimes " 
                 "(ringTimeName, weekDays, ringTime, ringPatternId) " 
                 "VALUES " 
                 "('" + newRingTimeName + "', "
                 "'" + weekDays + "', "
                 "'" + newRingTime + "', "
                 "'" + newRingPatternId + "')"
                 )
        try: # insert ring time in to db
            result, rowCount = db_query(cursor, query, verbose) # run query
        except (MySQLdb.IntegrityError) as e: # time name already in database
            print ("Error: <br>\nThere was already a time with that name. "
                   "<br>\n    Time not added "
                   "<br>\n%s" % e
                   )
        except MySQLdb.Error as e:
            print "<br>\nError: Could not add time <br>\n%s" % e
            print "<br>\nSQL: %s" % query
        else:
            print "<br>\nAdded new ring time"
            
elif updateRingTimeId: # update ring time
    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", updateRingTimeName):
        print ("Error: <br>\nIllegal characters in name!: '" + updateRingTimeName + "' "
               "<br>\nNo special characters (including Swedish etc.) allowed "
               "<br>\nOnly characters, digits, spaces and ,. allowed "
               "<br>\nMax 100 characters!"
               )
    elif not re.match("^[0-9:]{1,100}$", updateRingTime):
        print ("Error: <br>\nIllegal characters in time!: '" + updateRingTime + "' "
               "<br>\nOnly digits and : allowed "
               )
    elif len(updateRingTime.replace(' ', '').split(",")) % 2 == 0:
        print ("<br>\nError: <br>\nTime has an even set of times!: '" + updateRingTime + "' " 
               "<br>\nMust be an odd set of times "
               "<br>\nEg. '20' or '10, 5, 10' and so on"
               )
    else:
        query = ("UPDATE ringTimes SET "
                 "ringTimeName = '" + updateRingTimeName + "', "
                 "ringTime = '" + updateRingTime + "' "
                 "WHERE "
                 "ringTimeId = '%s'" % updateRingTimeId)
        try: # update ring time
            result, rowCount = db_query(cursor, query, verbose) # run query
        except (MySQLdb.IntegrityError) as e: # time name already in database
            print ("Error: <br>\nThere was already a time with that name. "
                   "<br>\nTime not updated "
                   "<br>\n%s>" % e
                   )
        except MySQLdb.Error as e:
            print "<br>\nError: Could not update time <br>\n%s" % e
            print "<br>\nSQL: %s" % query
        else:
            if rowCount:
                print "\n<br>Updated ring time with id = %s" % updateRingTimeId

def pageBody():

    # get ring times
    query = ("SELECT ringTimeId, ringTimeName, weekDays, ringTime, ringPatternId "
             "FROM ringTimes"
             )
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount: # display ring times in a table
        print '<br>\n<br>\n'
        print '<table style="width:100%">'
        print '<tr>'
        print '<th>Id</th>' 
        print '<th>Time name</th>'
        print '<th>Ring time</th>'
        print '<th>Ring pattern id</th>'
        print '<th>Ring pattern name</th>'
        print '<th>Ring pattern</th>'
        for dayNumber in range(0, 7):
            print '<th>%s</th>' % day_name[int(dayNumber)]
        
        print '<th></th>'
        print '<th></th>'
        print '</tr>'

        for row in result:
            ringTimeId = row[0]
            ringTimeName = row[1]
            weekDays = row[2]
            ringTime = row[3]
            ringPatternId = row[4]
            
            if editRingTimeId: # this is the ringTime we are about to edit
                newRingTimeName = ringTimeName
                newRingTime = ringTime
            
            print '<tr>'
            print '<th>%s</th>' % ringTimeId
            print '<th>%s</th>' % ringTimeName.encode('Latin1')
            print '<th>%s</th>' % ringTime
            print '<th>%s</th>' % ringPatternId
            # get ring patterns
            query = ("SELECT ringPatternName, ringPattern FROM ringPatterns "
                     "WHERE ringPatternID = '" + str(ringPatternId) + "'"
                     )
            result, rowCount = db_query(cursor, query, verbose)  # run query
            if rowCount:
                for row in result:
                    ringPatternName = row[0]
                    ringPattern = row[1]
            print '<th>%s</th>' % ringPatternName
            print '<th>%s</th>' % ringPattern
            for dayNumber in range(0, 7): # print day name
                if str(weekDays)[dayNumber] == "1":
                    print '<th>On</th>'
                else:
                    print '<th>Off</th>'
            print '<th><a href="ringTimes.py?deleteRingTimeId=%s">Delete</a></th>' % ringTimeId
            print '<th><a href="ringTimes.py?editRingTimeId=%s">Edit</a></th>' % ringTimeId
            print '</tr>'
            
        print '</table'
        
    if editRingTimeId:
        print '\n<br><br>'
        print '<h3>Edit ring time</h3>'
        
        print '<form action="/ringTimes.py">'
        
        print 'Time id:<br>'
        print '<input type="text" name="updateRingTimeId" value="%s">' % editRingTimeId
        
        print '<br><br><br>'
        print 'Ring time name:<br>'
        print '<input type="text" name="updateRingTimeName" value="%s">' % newRingTimeName
        print ('State a name for your ring time. <br><br>'
               '\nMax 100 characters. <br>'
               )
        
        print '<br><br>'
        print 'Ring time:<br>'
        print '<input type="text" name="updateRingTime" value="%s">' % newRingTime
        print ('State time in the form "hh:mm". <br>'
               )
        
        print '<br><br>'
        print '<input type="submit" value="Submit">'
        print '</form>'
            
    if addRingTime: # display form to add ring time
        print '\n<br><br>'
        print '<h3>Add ring time</h3>'
        
        print '<form action="/ringTimes.py">'
        
        print 'Ring time name:<br>'
        print '<input type="text" name="newRingTimeName" value="Time name">'
        print ('State a name for your ring time. <br><br>'
               '\nMax 100 characters. <br>'
               )
        
        print '<br><br>'
        print 'Ring time:<br>'
        print '<input type="text" name="newRingTime" value="Ring time">'
        print ('State time in the form "hh:mm". <br>'
               )
        
        print '<br><br>'
        print 'Choose ring pattern:<br>'
        print '<select name="newRingPatternId">'
        # get ring patterns
        query = ("SELECT ringPatternId, ringPatternName, ringPattern FROM ringPatterns")
        result, rowCount = db_query(cursor, query, verbose)  # run query
        if rowCount:
            for row in result:
                ringPatternId = row[0]
                ringPatternName = row[1]
                ringPattern = row[2]
                print ('<option value="%s">%s: %s, %s</option>'
                        % (ringPatternId, ringPatternId, ringPatternName, ringPattern)
                        )
        print '</select>'
        
        print '<br><br>'
        for dayNumber in range(0, 7):
            print ('<input type="checkbox" name="%s" value="1"> %s<br>' 
                    % (day_name[int(dayNumber)], day_name[int(dayNumber)])
                    )        
        print '<br><br>'
        print '<input type="submit" value="Submit">'
        print '</form>'
    else:
        print '\n<br>'
        print '<br>\n<a href="ringTimes.py?addRingTime=1">Add another ring time</a>'
    
    print '\n<br>'
    print '<br>\n<a href="index.py">Home</a>'
                
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