#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi, MySQLdb, re
import cgitb; cgitb.enable()  # for troubleshooting

from modules import (htmlFormEscape, webPageFooter, webPageHeader, 
                     db_connect, db_create_cursor, db_close_cursor, db_disconnect, db_query)

addRingPattern = False # will display form to add ring pattern

editRingPatternId = "" # this ring pattern will be edited

newRingPatternName = "" # new pattern will be inserted
newRingPattern = ""

updateRingPatternId = "" # this ring pattern will be updated
updateRingPatternName = ""
updateRingPattern = ""

deleteRingPatternId = "" # this ring pattern will be deleted

verbose = False

fs = cgi.FieldStorage()

print "Content-type: text/html"
print

print """
<html>

<head><title>piSchoolBell - ring patterns</title></head>

<style>
table, th, td {
    border: 1px solid black;
}
</style>
 
<body>
 
<h3> piSchoolBell - ring patterns</h3>
"""


# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx)

# handle inputs
for key in fs.keys():
    if key == "deleteRingPatternId": # delete ring pattern
        deleteRingPatternId = fs[key].value
        
    elif key == "editRingPatternId": # display form to edit ring pattern
        editRingPatternId = fs[key].value
        
    elif key == "addRingPattern" and fs[key].value == "1": # display form to add new ring pattern
        addRingPattern = True
        
    elif key == "newRingPatternName": # add ring pattern 
        newRingPatternName = fs[key].value
    elif key == "newRingPattern":
        newRingPattern = fs[key].value
        
    elif key == "updateRingPatternId": # update ring pattern 
        updateRingPatternId = fs[key].value    
    elif key == "updateRingPatternName": 
        updateRingPatternName = fs[key].value
    elif key == "updateRingPattern":
        updateRingPattern = fs[key].value
        
if deleteRingPatternId: # delete ring pattern
    query = ("SELECT ringTimeId, ringTimeName, ringTime FROM ringTimes WHERE ringPatternId = '%s'" % deleteRingPatternId)
    try:
        result, rowCount = db_query(cursor, query, verbose)  # run query
    except MySQLdb.Error as e:
        print "<br>\nError: Could not run query <br>\n%s" % e
        print "<br>\nSQL: %s" % query
    else:
        if rowCount:
            print ("<br>\nError: Could not delete ring pattern "
                   "<br>\nIt is being used at the following ring times: "
                   )
            for row in result:
                ringTimeId = row[0]
                ringTimeName = row[1]
                ringTime = row[2]
                print "<br><br>\nId: %s <br>\n%s, %s" % (ringTimeId, ringTimeName, ringTime) 
        else:
            query = ("DELETE FROM ringPatterns WHERE ringPatternId = '%s'" % deleteRingPatternId)
            try:
                result, rowCount = db_query(cursor, query, verbose)  # run query
            except MySQLdb.Error as e:
                print "<br>\nError: Could not delete pattern <br>\n%s" % e
                print "<br>\nSQL: %s" % query
            else:
                if rowCount:
                    print "\n<br>Deleted ring pattern with id = %s" % deleteRingPatternId

elif newRingPatternName: # add ring pattern
    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", newRingPatternName):
        print ("<br>\nError: <br>\nIllegal characters in name - " + newRingPatternName + " "
               "<br>\nNo special characters (including Swedish etc.) allowed "
               "<br>\nOnly characters, digits, spaces and ,. allowed "
               "<br>\nMax 100 characters"
               )
    elif not re.match("^[0-9, ]{1,100}$", newRingPattern):
        print ("<br>\nError: <br>\nIllegal characters in pattern - " + newRingPattern + " " 
               "<br>\nOnly digits, spaces and , allowed "
               "<br>\nMax 100 characters"
               )
    elif len(newRingPattern.replace(' ', '').split(",")) % 2 == 0:
        print ("<br>\nError: <br>\nPattern has an even set of times - " + newRingPattern + " " 
               "<br>\nMust be an odd set of times "
               "<br>\nEg. '20' or '10, 5, 10' and so on"
               )
    else:
        query = ("INSERT INTO ringPatterns " 
                 "(ringPatternName, ringPattern) " 
                 "VALUES " 
                 "('" + newRingPatternName + "', "
                 "'" + newRingPattern + "')"
                 )
        try: # insert ring pattern in to db
            result, rowCount = db_query(cursor, query, verbose) # run query
        except (MySQLdb.IntegrityError) as e: # pattern name already in database
            print ("Error: <br>\nThere was already a pattern with that name. "
                   "<br>\n    Pattern not added "
                   "<br>\n%s" % e
                   )
        except MySQLdb.Error as e:
            print "<br>\nError: Could not add pattern <br>\n%s" % e
            print "<br>\nSQL: %s" % query
        else:
            print "<br>\nAdded new ring pattern"
            
elif updateRingPatternId: # update ring pattern
    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", updateRingPatternName):
        print ("Error: <br>\nIllegal characters in name - " + updateRingPatternName + " "
               "<br>\nNo special characters (including Swedish etc.) allowed "
               "<br>\nOnly characters, digits, spaces and ,. allowed "
               "<br>\nMax 100 characters!"
               )
    elif not re.match("^[0-9, ]{1,100}$", updateRingPattern):
        print ("Error: <br>\nIllegal characters in pattern - " + updateRingPattern + " "
               "<br>\nOnly digits, spaces and , allowed "
               "<br>\nMax 100 characters!"
               )
    elif len(updateRingPattern.replace(' ', '').split(",")) % 2 == 0:
        print ("<br>\nError: <br>\nPattern has an even set of times - " + updateRingPattern + " " 
               "<br>\nMust be an odd set of times "
               "<br>\nEg. '20' or '10, 5, 10' and so on"
               )
    else:
        query = ("UPDATE ringPatterns SET "
                 "ringPatternName = '" + updateRingPatternName + "', "
                 "ringPattern = '" + updateRingPattern + "' "
                 "WHERE "
                 "ringPatternId = '%s'" % updateRingPatternId)
        try: # update ring pattern
            result, rowCount = db_query(cursor, query, verbose) # run query
        except (MySQLdb.IntegrityError) as e: # pattern name already in database
            print ("Error: <br>\nThere was already a pattern with that name. "
                   "<br>\nPattern not updated "
                   "<br>\n%s>" % e
                   )
        except MySQLdb.Error as e:
            print "<br>\nError: Could not update pattern <br>\n%s" % e
            print "<br>\nSQL: %s" % query
        else:
            if rowCount:
                print "\n<br>Updated ring pattern with id = %s" % updateRingPatternId

def pageLinks():
    
    print '<br>\n<a href="ringPatterns.py">Reset page</a>'
    
    print '&emsp;<a href="ringPatterns.py?addRingPattern=1">Add another ring pattern</a>'
    
    print '<br>\n'
    print '<br>\n<a href="index.py">Home</a>'
    
    print '<br>\n'
    print '<br>\n<a href="upcomingRings.py">Upcoming rings</a>'
    
    #print '<br>\n'
    print '<br>\n<a href="ringTimes.py">Ring times</a>'
    
    #print '<br>\n'
    print '<br>\n<a href="schoolBreaks.py">Breaks</a>'
    
    #print '<br>\n'
    #print '<br>\n<a href="extraDays.py">Extra school days</a>'
    
    #print '<br>\n'
    #print '<br>\n<a href="ringPatterns.py">Ring patterns</a>'
        
    
def pageBody():

    # get ring patterns
    query = ("SELECT ringPatternId, ringPatternName, ringPattern FROM ringPatterns")
    
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount: # display ring patterns in a table
        print '<br>\n<br>\n'
        print '<table style="width:400px">'
        print '<tr>'
        print '<th>Id</th>' 
        print '<th>Pattern name</th>'
        print '<th>Pattern</th>'
        print '<th></th>'
        print '<th></th>'
        print '</tr>'

        for row in result:
            ringPatternId = row[0]
            ringPatternName = row[1]
            ringPattern = row[2]
            
            if editRingPatternId == str(ringPatternId): # this is the ringPattern we are about to edit
                editRingPatternName = ringPatternName
                editRingPattern = ringPattern
            
            print '<tr>'
            print '<th>%s</th>' % ringPatternId
            print '<th>%s</th>' % ringPatternName.encode('Latin1')
            print '<th>%s</th>' % ringPattern
            print '<th><a href="ringPatterns.py?deleteRingPatternId=%s">Delete</a></th>' % ringPatternId
            print '<th><a href="ringPatterns.py?editRingPatternId=%s">Edit</a></th>' % ringPatternId
            print '</tr>'
            
        print '</table'
        
    if editRingPatternId:
        print '\n<br><br>'
        print '<h3>Edit ring pattern</h3>'
        print '<form action="/ringPatterns.py">'
        print 'Pattern id:<br>'
        print '<input type="text" name="updateRingPatternId" value="%s">' % editRingPatternId
        print '<br><br><br>'
        print 'Ring pattern name:<br>'
        print '<input type="text" name="updateRingPatternName" value="%s">' % editRingPatternName
        print ('State a name for your ring pattern. <br><br>'
               '\nMax 100 characters. <br>'
               )
        print '<br><br>'
        print 'Ring pattern:<br>'
        print '<input type="text" name="updateRingPattern" value="%s">' % editRingPattern
        print ('State pattern in 1/10 of a second. <br><br>'
               '\nSeparate values by commas. <br>'
               '\nFirst number is ring time, second is pause, third is ring time and so on. <br>'
               '\nIt must be an odd number of values. <br>'
               '\nOnly digits, commas and spaces are allowed. <br>'
               )
        print '<br><br>'
        print '<input type="submit" value="Submit">'
        print '</form>'
            
    if addRingPattern: # display form to add ring pattern
        print '\n<br><br>'
        print '<h3>Add ring pattern</h3>'
        print '<form action="/ringPatterns.py">'
        print 'Ring pattern name:<br>'
        print '<input type="text" name="newRingPatternName" value="Pattern name">'
        print ('State a name for your ring pattern. <br><br>'
               '\nMax 100 characters. <br>'
               )
        print '<br><br>'
        print 'Ring pattern:<br>'
        print '<input type="text" name="newRingPattern" value="Ring pattern">'
        print ('State pattern in 1/10 of a second. <br><br>'
               '\nSeparate values by commas. <br>'
               '\nFirst number is ring time, second is pause, third is ring time and so on. <br>'
               '\nIt must be an odd number of values. <br>'
               '\nOnly digits, commas and spaces are allowed. <br>'
               )
        print '<br><br>'
        print '<input type="submit" value="Submit">'
        print '</form>'
                
if __name__ == '__main__':
    webPageHeader()
    pageLinks()
    pageBody()
    print "<br>\n"
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