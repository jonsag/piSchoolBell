#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi, MySQLdb, re
import cgitb; cgitb.enable()  # for troubleshooting

from datetime import datetime

from modules import (htmlFormEscape, validateDate, webPageFooter, webPageHeader, 
                     db_connect, db_create_cursor, db_close_cursor, db_disconnect, db_query)

addSchoolBreak = False # will display form to add break

editSchoolBreakId = "" # this break will be edited

newSchoolBreakName = "" # new break will be inserted
newStartDate = ""
newEndDate = ''

updateSchoolBreakId = "" # this break will be updated
updateSchoolBreakName = ""
updateStartDate = ""
updateEndDate = ''

deleteSchoolBreakId = "" # this break will be deleted

verbose = False

fs = cgi.FieldStorage()

print "Content-type: text/html"
print

print """
<html>

<head><title>piSchoolBell - breaks</title></head>

<style>
table, th, td {
    border: 1px solid black;
}
</style>
 
<body>
 
<h3> piSchoolBell - breaks</h3>
"""


# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx, verbose)

# handle inputs
for key in fs.keys():
    if key == "deleteSchoolBreakId": # delete break
        deleteSchoolBreakId = fs[key].value
        
    elif key == "editSchoolBreakId": # display form to edit break
        editSchoolBreakId = fs[key].value
        
    elif key == "addSchoolBreak" and fs[key].value == "1": # display form to add new break
        addSchoolBreak = True
        
    elif key == "newSchoolBreakName": # add break 
        newSchoolBreakName = fs[key].value
    elif key == "newStartDate":
        newStartDate = fs[key].value
    elif key == "newEndDate":
        newEndDate = fs[key].value
        
    elif key == "updateSchoolBreakId": # update break 
        updateSchoolBreakId = fs[key].value    
    elif key == "updateSchoolBreakName": 
        updateSchoolBreakName = fs[key].value
    elif key == "updateStartDate":
        updateStartDate = fs[key].value
    elif key == "updateEndDate":
        updateEndDate = fs[key].value
        
# get current time
dateTimeNow = datetime.now()
dateNow = str(dateTimeNow.strftime('%Y-%m-%d'))
        
if deleteSchoolBreakId: # delete break
        query = ("DELETE FROM breaks WHERE breakId = '%s'" % deleteSchoolBreakId)
        try:
            result, rowCount = db_query(cursor, query, verbose)  # run query
        except MySQLdb.Error as e:
            print "\n<br>Error: Could not delete break \n<br>%s" % e
            print "\n<br>SQL: %s" % query
        else:
            if rowCount:
                print "\n<br>Deleted break with id = %s" % deleteSchoolBreakId

elif newSchoolBreakName: # add break
    if newEndDate == '': # no end date stated
        newEndDate = newStartDate
        
    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", newSchoolBreakName):
        print ("\n<br>Error: \n<br>Illegal characters in name - " + newSchoolBreakName + " "
               "\n<br>No special characters (including Swedish etc.) allowed "
               "\n<br>Only characters, digits, spaces and ,. allowed "
               "\n<br>Max 100 characters"
               )
    elif not re.match("^[0-9-]{1,10}$", newStartDate) or not validateDate(newStartDate, verbose):
        print ("\n<br>Error: \n<br>Illegal date, characters or length in start date - " + newStartDate + " " 
               "\n<br>Must be in the form YY-MM-DD"
               "\n<br>Only digits, spaces and - allowed "
               "\n<br>Max 100 characters"
               )
    elif not re.match("^[0-9-]{1,10}$", newEndDate) or not validateDate(newEndDate, verbose):
        print ("\n<br>Error: \n<br>Illegal date, characters or length in end date - " + newEndDate + " "
               "\n<br>Must be in the form YY-MM-DD" 
               "\n<br>Only digits, spaces and - allowed "
               "\n<br>Max 100 characters"
               )
    #elif newStartDate < dateNow:
    #    print ("\n<br>Error: \n<br>Start date occurs earlier than today - " + newStartDate + " < " + dateNow + " "
    #           )
    elif newEndDate < dateNow:
        print ("\n<br>Error: \n<br>End date occurs earlier than today - " + newEndDate + " < " + dateNow + " "
               )
    elif newEndDate < newStartDate:
        print ("\n<br>Error: \n<br>End date occurs earlier than start date - " + newEndDate + " < " + newStartDate + " "
               )
    elif newEndDate < dateNow:
        print ("\n<br>Error: \n<br>End date occurs earlier than today - " + newEndDate + " < " + dateNow + " "
               )
    else:
        query = ("INSERT INTO breaks " 
                 "(breakName, startDate, endDate) " 
                 "VALUES " 
                 "('" + newSchoolBreakName + "', "
                 "'" + newStartDate + "', "
                 "'" + newEndDate + "')"
                 )
        try: # insert break in to db
            result, rowCount = db_query(cursor, query, verbose) # run query
        except (MySQLdb.IntegrityError) as e: # break name already in database
            print ("Error: \n<br>There was already a break with that name. "
                   "\n<br>    Pattern not added "
                   "\n<br>%s" % e
                   )
        except MySQLdb.Error as e:
            print "\n<br>Error: Could not add break \n<br>%s" % e
            print "\n<br>SQL: %s" % query
        else:
            print "\n<br>Added new break"
            
elif updateSchoolBreakId: # update break
    if updateEndDate == '': # no end date stated
        updateEndDate = updateStartDate
    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", updateSchoolBreakName):
        print ("Error: \n<br>Illegal characters in name - " + updateSchoolBreakName + " "
               "\n<br>No special characters (including Swedish etc.) allowed "
               "\n<br>Only characters, digits, spaces and ,. allowed "
               "\n<br>Max 100 characters!"
               )
    elif not re.match("^[0-9-]{1,10}$", updateStartDate) or not validateDate(updateStartDate, verbose):
        print ("Error: \n<br>Illegal date, characters or length in start date - " + updateStartDate + " "
               "\n<br>Must be in the form YY-MM-DD"
               "\n<br>Only digits, spaces and , allowed "
               "\n<br>Max 100 characters!"
               )
    elif not re.match("^[0-9-]{1,10}$", updateEndDate) or not validateDate(updateEndDate, verbose):
        print ("Error: \n<br>Illegal date, characters or length in end date - " + updateEndDate + " "
               "\n<br>Must be in the form YY-MM-DD"
               "\n<br>Only digits, spaces and , allowed "
               "\n<br>Max 100 characters!"
               )
    #elif updateStartDate < dateNow:
    #    print ("\n<br>Error: \n<br>Start date occurs earlier than today - " + updateStartDate + " < " + dateNow + " "
    #           )
    elif updateEndDate < dateNow:
        print ("\n<br>Error: \n<br>End date occurs earlier than today - " + updateEndDate + " < " + dateNow + " "
               )
    elif updateEndDate < updateStartDate:
        print ("\n<br>Error: \n<br>End date occurs earlier than start date - " + updateEndDate + " < " + updateStartDate + " "
               )
    elif updateEndDate < dateNow:
        print ("\n<br>Error: \n<br>End date occurs earlier than today - " + updateEndDate + " < " + dateNow + " "
               )
    else:
        query = ("UPDATE breaks SET "
                 "breakName = '" + updateSchoolBreakName + "', "
                 "startDate = '" + updateStartDate + "', "
                 "endDate = '" + updateEndDate + "' "
                 "WHERE "
                 "breakId = '%s'" % updateSchoolBreakId)
        try: # update break
            result, rowCount = db_query(cursor, query, verbose) # run query
        except (MySQLdb.IntegrityError) as e: # break name already in database
            print ("Error: \n<br>There was already a break with that name. "
                   "\n<br>Pattern not updated "
                   "\n<br>%s>" % e
                   )
        except MySQLdb.Error as e:
            print "\n<br>Error: Could not update break \n<br>%s" % e
            print "\n<br>SQL: %s" % query
        else:
            if rowCount:
                print "\n<br>Updated break with id = %s" % updateSchoolBreakId

def pageLinks():
    
    print '\n<br><a href="schoolBreaks.py">Reset page</a>'
    
    print '&emsp;<a href="schoolBreaks.py?addSchoolBreak=1">Add another break</a>'
    
    print '\n<br>'
    print '\n<br><a href="index.py">Home</a>'
    
    print '\n<br>'
    print '\n<br><a href="upcomingRings.py">Upcoming rings</a>'
    
    #print '\n<br>'
    print '\n<br><a href="ringTimes.py">Ring times</a>'
    
    #print '\n<br>'
    #print '\n<br><a href="schoolBreaks.py">Breaks</a>'
    
    #print '\n<br>'
    #print '\n<br><a href="extraDays.py">Extra school days</a>'
    
    #print '\n<br>'
    print '\n<br><a href="ringPatterns.py">Ring patterns</a>'
        

def pageBody():

    # get breaks
    query = ("SELECT breakId, breakName, startDate, endDate FROM breaks ORDER BY startDate ASC")
    
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount: # display breaks in a table
        print '\n<br>\n<br>'
        print '<table style="width:400px">'
        print '<tr>'
        print '<th>Id</th>' 
        print '<th>Break name</th>'
        print '<th>Start date</th>'
        print '<th>End date</th>'
        print '<th></th>'
        print '<th></th>'
        print '</tr>'

        for row in result:
            schoolBreakId = row[0]
            schoolBreakName = row[1]
            startDate = row[2]
            endDate = row[3]
            
            if editSchoolBreakId == str(schoolBreakId): # this is the schoolBreak we are about to edit
                editSchoolBreakName = schoolBreakName
                editStartDate = startDate
                editEndDate = endDate
            
            print '<tr>'
            print '<th>%s</th>' % schoolBreakId
            print '<th>%s</th>' % schoolBreakName.encode('Latin1')
            print '<th>%s</th>' % startDate
            print '<th>%s</th>' % endDate
            print '<th><a href="schoolBreaks.py?deleteSchoolBreakId=%s">Delete</a></th>' % schoolBreakId
            print '<th><a href="schoolBreaks.py?editSchoolBreakId=%s">Edit</a></th>' % schoolBreakId
            print '</tr>'
            
        print '</table'
        
    if editSchoolBreakId:
        print '\n<br><br>'
        print '<h3>Edit break</h3>'
        
        print '<form action="/schoolBreaks.py">'
        print 'Pattern id:<br>'
        print '<input type="text" name="updateSchoolBreakId" value="%s">' % editSchoolBreakId
        
        print '<br><br><br>'
        print 'Break name:<br>'
        print '<input type="text" name="updateSchoolBreakName" value="%s">' % editSchoolBreakName
        print ('State a name for your break. <br><br>'
               '\nMax 100 characters. <br>'
               )
        
        print '<br><br>'
        print 'Start date:<br>'
        print '<input type="text" name="updateStartDate" value="%s">' % editStartDate
        print ('State date in the form: YY-MM-DD. <br><br>'
               '\nOnly digits and - are allowed. <br>'
               )
        
        print '<br><br>'
        print 'End date:<br>'
        print '<input type="text" name="updateEndDate" value="%s">' % editEndDate
        print ('State date in the form: YY-MM-DD. <br><br>'
               '\nOnly digits and - are allowed. <br>'
               )
        
        print '<br><br>'
        print '<input type="submit" value="Submit">'
        print '</form>'
            
    if addSchoolBreak: # display form to add break
        print '\n<br><br>'
        print '<h3>Add break</h3>'
        
        print '<form action="/schoolBreaks.py">'
        print 'Break name:<br>'
        print '<input type="text" name="newSchoolBreakName" value="Break name">'
        print ('State a name for your break. <br><br>'
               '\nMax 100 characters. <br>'
               )
        
        dateTimeNow = datetime.now()
        dateNow = str(dateTimeNow.strftime('%Y-%m-%d'))
        print '<br><br>'
        print 'Start date:<br>'
        print '<input type="text" name="newStartDate" value="%s">' % dateNow
        print ('State date in the form: YY-MM-DD. <br><br>'
               '\nOnly digits and - are allowed. <br>'
               )

        print '<br><br>'
        print 'End date:<br>'
        print '<input type="text" name="newEndDate" value="%s">' % dateNow
        print ('State date in the form: YY-MM-DD. <br><br>'
               '\nOnly digits and - are allowed. <br>'
               )
                
        print '<br><br>'
        print '<input type="submit" value="Submit">'
        print '</form>'
                
if __name__ == '__main__':
    webPageHeader()
    pageLinks()
    pageBody()
    print "\n<br>"
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