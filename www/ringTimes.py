#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi, MySQLdb, re, sys
import cgitb

cgitb.enable()  # for troubleshooting

from datetime import datetime

from modules import (
    htmlFormEscape,
    validateTime,
    getDayName,
    webPageFooter,
    webPageHeader,
    db_connect,
    db_create_cursor,
    db_close_cursor,
    db_disconnect,
    db_query,
)

addRingTime = False  # will display form to add ring time

editRingTimeId = ""  # this ring time will be edited

newRingTimeName = ""  # new time will be inserted
newRingTime = ""

updateRingTimeId = ""  # this ring time will be updated
updateRingTimeName = ""
updateRingTime = ""

deleteRingTimeId = ""  # this ring time will be deleted

weekDays = list("0000000")  # weekDays string

verbose = False

fs = cgi.FieldStorage()

print("Content-type: text/html")
print()

print("""
<html>

<head><title>piSchoolBell - ring times</title></head>

<style>
table, th, td {
    border: 1px solid black;
}
</style>
 
<body>
 
<h3> piSchoolBell - ring times</h3>
""")


# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx, verbose)

for key in list(fs.keys()):
    if key == "deleteRingTimeId":  # delete ring time
        deleteRingTimeId = fs[key].value

    elif key == "editRingTimeId":  # display form to edit ring time
        editRingTimeId = fs[key].value

    elif (
        key == "addRingTime" and fs[key].value == "1"
    ):  # display form to add new ring time
        addRingTime = True

    elif key == "newRingTimeName":  # add ring time
        newRingTimeName = fs[key].value
    elif key == "newRingTime":
        newRingTime = fs[key].value
    elif key == "newWeekDays":
        newWeekDays = fs[key].value
    elif key == "newRingPatternId":
        newRingPatternId = fs[key].value

    elif key == "updateRingTimeId":  # update ring time
        updateRingTimeId = fs[key].value
    elif key == "updateRingTimeName":
        updateRingTimeName = fs[key].value
    elif key == "updateRingTime":
        updateRingTime = fs[key].value

    elif key == "Monday":  # weekdays
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

weekDays = "".join(weekDays)

# handle inputs
if deleteRingTimeId:  # delete ring time
    query = "DELETE FROM ringTimes WHERE ringTimeId = '%s'" % deleteRingTimeId
    try:
        result, rowCount = db_query(cursor, query, verbose)  # run query
    except MySQLdb.Error as e:
        print("\n<br>Error: Could not delete time \n<br>%s" % e)
        print("\n<br>SQL: %s" % query)
    else:
        if rowCount:
            print("\n<br>Deleted ring time with id = %s" % deleteRingTimeId)

elif newRingTimeName:  # add ring time
    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", newRingTimeName):
        print((
            "\n<br>Error: \n<br>Illegal characters in name!: '" + newRingTimeName + "' "
            "\n<br>No special characters (including Swedish etc.) allowed "
            "\n<br>Only characters, digits, spaces and ,. allowed "
            "\n<br>Max 100 characters"
        ))
    elif not re.match("^[0-9:]{1,5}$", newRingTime) or not validateTime(
        newRingTime, verbose
    ):
        print((
            "\n<br>Error: \n<br>Illegal time, characters or length in: '"
            + newRingTime
            + "'! "
            "\n<br>Must be in the form HH:MM "
            "\n<br>Only digits and : allowed "
        ))
    else:
        query = (
            "INSERT INTO ringTimes "
            "(ringTimeName, weekDays, ringTime, ringPatternId) "
            "VALUES "
            "('" + newRingTimeName + "', "
            "'" + weekDays + "', "
            "'" + newRingTime + "', "
            "'" + newRingPatternId + "')"
        )
        try:  # insert ring time in to db
            result, rowCount = db_query(cursor, query, verbose)  # run query
        except (MySQLdb.IntegrityError) as e:  # time name already in database
            print((
                "Error: \n<br>There was already a time with that name. "
                "\n<br>    Time not added "
                "\n<br>%s" % e
            ))
        except MySQLdb.Error as e:
            print("\n<br>Error: Could not add time \n<br>%s" % e)
            print("\n<br>SQL: %s" % query)
        else:
            print("\n<br>Added new ring time")

elif updateRingTimeId:  # update ring time
    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", updateRingTimeName):
        print((
            "Error: \n<br>Illegal characters in name!: '" + updateRingTimeName + "' "
            "\n<br>No special characters (including Swedish etc.) allowed "
            "\n<br>Only characters, digits, spaces and ,. allowed "
            "\n<br>Max 100 characters!"
        ))
    elif not re.match("^[0-9:]{1,5}$", updateRingTime) or not validateTime(
        updateRingTime, verbose
    ):
        print((
            "Error: \n<br>Illegal time, characters or length in: '"
            + updateRingTime
            + "'! "
            "\n<br>Must be in the form HH:MM "
            "\n<br>Only digits and : allowed "
        ))
    else:
        query = (
            "UPDATE ringTimes SET "
            "ringTimeName = '" + updateRingTimeName + "', "
            "ringTime = '" + updateRingTime + "', "
            "ringPatternID = '" + newRingPatternId + "', "
            "weekDays = '" + weekDays + "' "
            "WHERE "
            "ringTimeId = '%s'" % updateRingTimeId
        )
        try:  # update ring time
            result, rowCount = db_query(cursor, query, verbose)  # run query
        except (MySQLdb.IntegrityError) as e:  # time name already in database
            print((
                "Error: \n<br>There was already a time with that name. "
                "\n<br>Time not updated "
                "\n<br>%s>" % e
            ))
        except MySQLdb.Error as e:
            print("\n<br>Error: Could not update time \n<br>%s" % e)
            print("\n<br>SQL: %s" % query)
        else:
            if rowCount:
                print("\n<br>Updated ring time with id = %s" % updateRingTimeId)


def pageLinks():

    print('\n<br><a href="ringTimes.py">Reset page</a>')

    print('&emsp;<a href="ringTimes.py?addRingTime=1">Add another ring time</a>')

    print("\n<br>")
    print('\n<br><a href="index.py">Home</a>')

    print("\n<br>")
    print('\n<br><a href="upcomingRings.py">Upcoming rings</a>')

    # print '\n<br>'
    # print '\n<br><a href="ringTimes.py">Ring times</a>'

    # print '\n<br>'
    print('\n<br><a href="schoolBreaks.py">Breaks</a>')

    # print '\n<br>'
    # print '\n<br><a href="extraDays.py">Extra school days</a>'

    # print '\n<br>'
    print('\n<br><a href="ringPatterns.py">Ring patterns</a>')


def pageBody():

    # get ring times
    query = (
        "SELECT ringTimeId, ringTimeName, weekDays, TIME_FORMAT(ringTime, '%H:%i') as ringTime, ringPatternId "
        "FROM ringTimes ORDER BY ringTime ASC"
    )
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:  # display ring times in a table
        print("\n<br>\n<br>")
        print('<table style="width:100%">')
        print("<tr>")
        print("<th>Id</th>")
        print("<th>Time name</th>")
        print("<th>Ring time</th>")
        print("<th>Ring pattern id</th>")
        print("<th>Ring pattern name</th>")
        print("<th>Ring pattern</th>")
        for dayNumber in range(0, 7):
            print("<th>%s</th>" % getDayName(dayNumber, verbose))

        print("<th></th>")
        print("<th></th>")
        print("</tr>")

        for row in result:
            ringTimeId = row[0]
            ringTimeName = row[1]
            weekDays = row[2]
            ringTime = row[3]
            ringPatternId = row[4]

            if editRingTimeId == str(
                ringTimeId
            ):  # this is the ringTime we are about to edit
                editRingTimeName = ringTimeName
                editWeekDays = weekDays
                editRingTime = ringTime
                editRingPatternId = ringPatternId

            print("<tr>")
            print("<th>%s</th>" % ringTimeId)
            print("<th>%s</th>" % ringTimeName)
            print("<th>%s</th>" % ringTime)
            print("<th>%s</th>" % ringPatternId)
            # get ring patterns
            query = (
                "SELECT ringPatternName, ringPattern FROM ringPatterns "
                "WHERE ringPatternID = '" + str(ringPatternId) + "'"
            )
            result, rowCount = db_query(cursor, query, verbose)  # run query
            if rowCount:
                for row in result:
                    ringPatternName = row[0]
                    ringPattern = row[1]
            print("<th>%s</th>" % ringPatternName)
            print("<th>%s</th>" % ringPattern)
            for dayNumber in range(0, 7):  # print day name
                if weekDays[dayNumber] == "1":
                    print("<th>On</th>")
                else:
                    print("<th>Off</th>")
            print('<th><a href="ringTimes.py?deleteRingTimeId=%s">Delete</a></th>' % ringTimeId)
            print('<th><a href="ringTimes.py?editRingTimeId=%s">Edit</a></th>' % ringTimeId)
            print("</tr>")

        print("</table")

    if editRingTimeId:
        print("\n<br><br>")
        print("<h3>Edit ring time</h3>")

        print('<form action="/ringTimes.py">')

        print("Time id:<br>")
        print('<input type="text" name="updateRingTimeId" value="%s">' % editRingTimeId)

        print("<br><br><br>")
        print("Ring time name:<br>")
        print('<input type="text" name="updateRingTimeName" value="%s">' % editRingTimeName)
        print ("State a name for your ring time. <br><br>" "\nMax 100 characters. <br>")

        print("<br><br>")
        print("Ring time:<br>")
        print('<input type="text" name="updateRingTime" value="%s">' % editRingTime)
        print ('State time in the form "hh:mm". <br>')

        print("<br><br>")
        print("Choose ring pattern:<br>")
        print('<select name="newRingPatternId">')
        # get ring patterns
        query = "SELECT ringPatternId, ringPatternName, ringPattern FROM ringPatterns"
        result, rowCount = db_query(cursor, query, verbose)  # run query
        if rowCount:
            for row in result:
                ringPatternId = row[0]
                ringPatternName = row[1]
                ringPattern = row[2]

                isSelected = ""
                if ringPatternId == editRingPatternId:
                    isSelected = 'selected="selected"'

                print((
                    '<option value="%s" %s>%s: %s, %s</option>'
                    % (
                        ringPatternId,
                        isSelected,
                        ringPatternId,
                        ringPatternName,
                        ringPattern,
                    )
                ))
        print("</select>")

        print("<br><br>")
        for dayNumber in range(0, 7):

            isChecked = ""
            if str(editWeekDays)[dayNumber] == "1":
                isChecked = 'checked="checked"'

            print((
                '<input type="checkbox" name="%s" value="1" %s> %s<br>'
                % (
                    getDayName(dayNumber, verbose),
                    isChecked,
                    getDayName(dayNumber, verbose),
                )
            ))

        print("<br><br>")
        print('<input type="submit" value="Submit">')
        print("</form>")

    if addRingTime:  # display form to add ring time
        print("\n<br><br>")
        print("<h3>Add ring time</h3>")

        print('<form action="/ringTimes.py">')

        print("Ring time name:<br>")
        print('<input type="text" name="newRingTimeName" value="Time name">')
        print ("State a name for your ring time. <br><br>" "\nMax 100 characters. <br>")

        dateTimeNow = datetime.now()
        timeNow = dateTimeNow.strftime("%H:%M")
        print("<br><br>")
        print("Ring time:<br>")
        print('<input type="text" name="newRingTime" value="%s">' % timeNow)
        print ('State time in the form "hh:mm". <br>')

        print("<br><br>")
        print("Choose ring pattern:<br>")
        print('<select name="newRingPatternId">')
        # get ring patterns
        query = "SELECT ringPatternId, ringPatternName, ringPattern FROM ringPatterns"
        result, rowCount = db_query(cursor, query, verbose)  # run query
        if rowCount:
            for row in result:
                ringPatternId = row[0]
                ringPatternName = row[1]
                ringPattern = row[2]
                print((
                    '<option value="%s">%s: %s, %s</option>'
                    % (ringPatternId, ringPatternId, ringPatternName, ringPattern)
                ))
        print("</select>")

        print("<br><br>")
        for dayNumber in range(0, 7):

            isChecked = ""
            if dayNumber >= 0 and dayNumber <= 4:
                isChecked = 'checked="checked"'

            print((
                '<input type="checkbox" name="%s" value="1" %s> %s<br>'
                % (
                    getDayName(dayNumber, verbose),
                    isChecked,
                    getDayName(dayNumber, verbose),
                )
            ))

        print("<br><br>")
        print('<input type="submit" value="Submit">')
        print("</form>")


if __name__ == "__main__":
    webPageHeader()
    pageLinks()
    pageBody()
    print("\n<br>")
    pageLinks()
    webPageFooter()


# close cursor
db_close_cursor(cnx, cursor, verbose)

# close db
db_disconnect(cnx, verbose)

print("""
 

 
</body>

</html>
""")