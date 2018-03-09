#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi, MySQLdb
import cgitb; cgitb.enable()  # for troubleshooting

from modules import (db_connect, db_create_cursor, db_close_cursor, db_disconnect, db_query)

addRingPattern = False # will display for to add ring pattern

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
    query = ("DELETE FROM ringPatterns WHERE ringPatternId = '%s'" % deleteRingPatternId)
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:
        print "\n<br>"
        print "Deleted ring pattern with id = %s" % fs[key].value
        print "\n<br>"
elif newRingPatternName: # add ring pattern
    query = ("INSERT INTO ringPatterns " 
             "(ringPatternName, ringPattern) " 
             "VALUES " 
             "('" + newRingPatternName + "', "
             "'" + newRingPattern + "')"
             )
    try: # insert ring pattern in to db
        result, rowCount = db_query(cursor, query, verbose) # run query
    except (MySQLdb.IntegrityError) as e: # pattern name already in database
        print "Error: There was already a pattern with that name. <br>\n    Pattern not added. <br><br>"
elif updateRingPatternId: # delete ring pattern
    query = ("UPDATE ringPatterns SET "
             "ringPatternName = '" + updateRingPatternName + "', "
             "ringPattern = '" + updateRingPattern + "' "
             "WHERE "
             "ringPatternId = '%s'" % updateRingPatternId)
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:
        print "\n<br>"
        print "Updated ring pattern with id = %s" % updateRingPatternId
        print "\n<br>"

def pageBody():

    # get ring patterns
    query = ("SELECT ringPatternId, ringPatternName, ringPattern FROM ringPatterns")
    
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount: # display ring patterns in a table
        print '<br>\n'
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
            
            if editRingPatternId: # this is the ringPattern we are about to edit
                newRingPatternName = ringPatternName
                newRingPattern = ringPattern
            
            print '<tr>'
            print '<th>%s</th>' % ringPatternId
            print '<th>%s</th>' % ringPatternName
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
        print '<input type="text" name="updateRingPatternName" value="%s">' % newRingPatternName
        print ('State a name for your ring pattern. <br><br>'
               '\nMax 100 characters. <br>'
               )
        print '<br><br>'
        print 'Ring pattern:<br>'
        print '<input type="text" name="updateRingPattern" value="%s">' % newRingPattern
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
    else:
        print '\n<br>'
        print '<br>\n<a href="ringPatterns.py?addRingPattern=1">Add another ring pattern</a>'
    
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