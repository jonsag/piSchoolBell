#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi, MySQLdb, re
import cgitb

cgitb.enable()  # for troubleshooting

from modules import (
    htmlFormEscape,
    webPageFooter,
    webPageHeader,
    db_connect,
    db_create_cursor,
    db_close_cursor,
    db_disconnect,
    db_query,
)

addRingPattern = False  # will display form to add ring pattern

editRingPatternId = ""  # this ring pattern will be edited

newRingPatternName = ""  # new pattern will be inserted
newRingPattern = ""

updateRingPatternId = ""  # this ring pattern will be updated
updateRingPatternName = ""
updateRingPattern = ""

deleteRingPatternId = ""  # this ring pattern will be deleted

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
cursor = db_create_cursor(cnx, verbose)

# handle inputs
for key in fs.keys():
    if key == "deleteRingPatternId":  # delete ring pattern
        deleteRingPatternId = fs[key].value

    elif key == "editRingPatternId":  # display form to edit ring pattern
        editRingPatternId = fs[key].value

    elif (
        key == "addRingPattern" and fs[key].value == "1"
    ):  # display form to add new ring pattern
        addRingPattern = True

    elif key == "newRingPatternName":  # add ring pattern
        newRingPatternName = fs[key].value
    elif key == "newRingPattern":
        newRingPattern = fs[key].value

    elif key == "updateRingPatternId":  # update ring pattern
        updateRingPatternId = fs[key].value
    elif key == "updateRingPatternName":
        updateRingPatternName = fs[key].value
    elif key == "updateRingPattern":
        updateRingPattern = fs[key].value

if deleteRingPatternId:  # delete ring pattern
    query = (
        "SELECT ringTimeId, ringTimeName, ringTime FROM ringTimes WHERE ringPatternId = '%s'"
        % deleteRingPatternId
    )
    try:
        result, rowCount = db_query(cursor, query, verbose)  # run query
    except MySQLdb.Error as e:
        print "\n<br>Error: Could not run query \n<br>%s" % e
        print "\n<br>SQL: %s" % query
    else:
        if rowCount:
            print (
                "\n<br>Error: Could not delete ring pattern "
                "\n<br>It is being used at the following ring times: "
            )
            for row in result:
                ringTimeId = row[0]
                ringTimeName = row[1]
                ringTime = row[2]
                print "<br>\n<br>Id: %s \n<br>%s, %s" % (
                    ringTimeId,
                    ringTimeName,
                    ringTime,
                )
        else:
            query = (
                "DELETE FROM ringPatterns WHERE ringPatternId = '%s'"
                % deleteRingPatternId
            )
            try:
                result, rowCount = db_query(cursor, query, verbose)  # run query
            except MySQLdb.Error as e:
                print "\n<br>Error: Could not delete pattern \n<br>%s" % e
                print "\n<br>SQL: %s" % query
            else:
                if rowCount:
                    print "\n<br>Deleted ring pattern with id = %s" % deleteRingPatternId

elif newRingPatternName:  # add ring pattern
    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", newRingPatternName):
        print (
            "\n<br>Error: \n<br>Illegal characters in name - "
            + newRingPatternName
            + " "
            "\n<br>No special characters (including Swedish etc.) allowed "
            "\n<br>Only characters, digits, spaces and ,. allowed "
            "\n<br>Max 100 characters"
        )
    elif not re.match("^[0-9, ]{1,100}$", newRingPattern):
        print (
            "\n<br>Error: \n<br>Illegal characters in pattern - " + newRingPattern + " "
            "\n<br>Only digits, spaces and , allowed "
            "\n<br>Max 100 characters"
        )
    elif len(newRingPattern.replace(" ", "").split(",")) % 2 == 0:
        print (
            "\n<br>Error: \n<br>Pattern has an even set of times - "
            + newRingPattern
            + " "
            "\n<br>Must be an odd set of times "
            "\n<br>Eg. '20' or '10, 5, 10' and so on"
        )
    else:
        query = (
            "INSERT INTO ringPatterns "
            "(ringPatternName, ringPattern) "
            "VALUES "
            "('" + newRingPatternName + "', "
            "'" + newRingPattern + "')"
        )
        try:  # insert ring pattern in to db
            result, rowCount = db_query(cursor, query, verbose)  # run query
        except (MySQLdb.IntegrityError) as e:  # pattern name already in database
            print (
                "Error: \n<br>There was already a pattern with that name. "
                "\n<br>    Pattern not added "
                "\n<br>%s" % e
            )
        except MySQLdb.Error as e:
            print "\n<br>Error: Could not add pattern \n<br>%s" % e
            print "\n<br>SQL: %s" % query
        else:
            print "\n<br>Added new ring pattern"

elif updateRingPatternId:  # update ring pattern
    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", updateRingPatternName):
        print (
            "Error: \n<br>Illegal characters in name - " + updateRingPatternName + " "
            "\n<br>No special characters (including Swedish etc.) allowed "
            "\n<br>Only characters, digits, spaces and ,. allowed "
            "\n<br>Max 100 characters!"
        )
    elif not re.match("^[0-9, ]{1,100}$", updateRingPattern):
        print (
            "Error: \n<br>Illegal characters in pattern - " + updateRingPattern + " "
            "\n<br>Only digits, spaces and , allowed "
            "\n<br>Max 100 characters!"
        )
    elif len(updateRingPattern.replace(" ", "").split(",")) % 2 == 0:
        print (
            "\n<br>Error: \n<br>Pattern has an even set of times - "
            + updateRingPattern
            + " "
            "\n<br>Must be an odd set of times "
            "\n<br>Eg. '20' or '10, 5, 10' and so on"
        )
    else:
        query = (
            "UPDATE ringPatterns SET "
            "ringPatternName = '" + updateRingPatternName + "', "
            "ringPattern = '" + updateRingPattern + "' "
            "WHERE "
            "ringPatternId = '%s'" % updateRingPatternId
        )
        try:  # update ring pattern
            result, rowCount = db_query(cursor, query, verbose)  # run query
        except (MySQLdb.IntegrityError) as e:  # pattern name already in database
            print (
                "Error: \n<br>There was already a pattern with that name. "
                "\n<br>Pattern not updated "
                "\n<br>%s>" % e
            )
        except MySQLdb.Error as e:
            print "\n<br>Error: Could not update pattern \n<br>%s" % e
            print "\n<br>SQL: %s" % query
        else:
            if rowCount:
                print "\n<br>Updated ring pattern with id = %s" % updateRingPatternId


def pageLinks():

    print '\n<br><a href="ringPatterns.py">Reset page</a>'

    print '&emsp;<a href="ringPatterns.py?addRingPattern=1">Add another ring pattern</a>'

    print "\n<br>"
    print '\n<br><a href="index.py">Home</a>'

    print "\n<br>"
    print '\n<br><a href="upcomingRings.py">Upcoming rings</a>'

    # print '\n<br>'
    print '\n<br><a href="ringTimes.py">Ring times</a>'

    # print '\n<br>'
    print '\n<br><a href="schoolBreaks.py">Breaks</a>'

    # print '\n<br>'
    # print '\n<br><a href="extraDays.py">Extra school days</a>'

    # print '\n<br>'
    # print '\n<br><a href="ringPatterns.py">Ring patterns</a>'


def pageBody():

    # get ring patterns
    query = "SELECT ringPatternId, ringPatternName, ringPattern FROM ringPatterns"

    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:  # display ring patterns in a table
        print "\n<br>\n<br>"
        print '<table style="width:400px">'
        print "<tr>"
        print "<th>Id</th>"
        print "<th>Pattern name</th>"
        print "<th>Pattern</th>"
        print "<th></th>"
        print "<th></th>"
        print "</tr>"

        for row in result:
            ringPatternId = row[0]
            ringPatternName = row[1]
            ringPattern = row[2]

            if editRingPatternId == str(
                ringPatternId
            ):  # this is the ringPattern we are about to edit
                editRingPatternName = ringPatternName
                editRingPattern = ringPattern

            print "<tr>"
            print "<th>%s</th>" % ringPatternId
            print "<th>%s</th>" % ringPatternName.encode("Latin1")
            print "<th>%s</th>" % ringPattern
            print '<th><a href="ringPatterns.py?deleteRingPatternId=%s">Delete</a></th>' % ringPatternId
            print '<th><a href="ringPatterns.py?editRingPatternId=%s">Edit</a></th>' % ringPatternId
            print "</tr>"

        print "</table"

    if editRingPatternId:
        print "\n<br><br>"
        print "<h3>Edit ring pattern</h3>"
        print '<form action="/ringPatterns.py">'
        print "Pattern id:<br>"
        print '<input type="text" name="updateRingPatternId" value="%s">' % editRingPatternId
        print "<br><br><br>"
        print "Ring pattern name:<br>"
        print '<input type="text" name="updateRingPatternName" value="%s">' % editRingPatternName
        print (
            "State a name for your ring pattern. <br><br>" "\nMax 100 characters. <br>"
        )
        print "<br><br>"
        print "Ring pattern:<br>"
        print '<input type="text" name="updateRingPattern" value="%s">' % editRingPattern
        print (
            "State pattern in 1/10 of a second. <br><br>"
            "\nSeparate values by commas. <br>"
            "\nFirst number is ring time, second is pause, third is ring time and so on. <br>"
            "\nIt must be an odd number of values. <br>"
            "\nOnly digits, commas and spaces are allowed. <br>"
        )
        print "<br><br>"
        print '<input type="submit" value="Submit">'
        print "</form>"

    if addRingPattern:  # display form to add ring pattern
        print "\n<br><br>"
        print "<h3>Add ring pattern</h3>"
        print '<form action="/ringPatterns.py">'
        print "Ring pattern name:<br>"
        print '<input type="text" name="newRingPatternName" value="Pattern name">'
        print (
            "State a name for your ring pattern. <br><br>" "\nMax 100 characters. <br>"
        )
        print "<br><br>"
        print "Ring pattern:<br>"
        print '<input type="text" name="newRingPattern" value="Ring pattern">'
        print (
            "State pattern in 1/10 of a second. <br><br>"
            "\nSeparate values by commas. <br>"
            "\nFirst number is ring time, second is pause, third is ring time and so on. <br>"
            "\nIt must be an odd number of values. <br>"
            "\nOnly digits, commas and spaces are allowed. <br>"
        )
        print "<br><br>"
        print '<input type="submit" value="Submit">'
        print "</form>"


if __name__ == "__main__":
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