#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys, getopt, os

from datetime import datetime
from shutil import copy, copyfile

from modules import (
    db_connect,
    db_create_cursor,
    db_close_cursor,
    db_disconnect,
    db_query,
    tempDir,
    USBDir,
    labelMatch,
    findUSBMountPoint,
    logFile,
    gpioWatchLog,
    splitPath,
    displayOnLCD,
    tableSelection,
    onError,
    usage,
)

try:
    myopts, args = getopt.getopt(
        sys.argv[1:], "dr" "vh", ["dump", "read", "verbose", "help"]
    )

except getopt.GetoptError as e:
    onError(1, str(e))

# if len(sys.argv) == 1:  # no options passed
#    onError(2, 2)

dump = False
read = False
verbose = False

for option, argument in myopts:
    if option in ("-d", "--dump"):  # first line of LCD
        dump = True
    elif option in ("-r", "--read"):  # verbose output
        read = True
    elif option in ("-v", "--verbose"):  # verbose output
        verbose = True
    elif option in ("-h", "--help"):  # display help text
        usage(0)

if dump and read:
    onError(3, "You cannot state both '-d' ('--dump') and -r' ('--read')")


def dumpToFile():
    filesWritten = 0

    timeNow = datetime.today()
    timeStamp = timeNow.strftime("%Y%m%d%H%M%S")

    USBPath = findUSBMountPoint(USBDir, labelMatch, verbose)

    if not USBPath:
        LCDMessage = "No USB inserted"

        if verbose:
            print "\n*** Printing to LCD: \n    %s" % LCDMessage
        displayOnLCD("", LCDMessage, verbose)
        onError(5, "No matching USB mounted")
    else:
        displayOnLCD("", "Writing files...", verbose)

    # database
    outFilePath = os.path.join(tempDir, "piSchoolBellDb-%s.csv" % timeStamp)

    if verbose:
        print "\n*** Creating file %s ..." % outFilePath
    outFile = open(outFilePath, "a")

    # connect to database
    cnx = db_connect(verbose)

    # create cursor
    cursor = db_create_cursor(cnx, verbose)

    for table in ("breaks", "ringTimes", "ringPatterns", "days"):
        if verbose:
            print "\n*** Reading table %s..." % table

        selection = tableSelection(table, verbose)

        query = "SELECT " + selection + " FROM " + table + " "
        result, rowCount = db_query(cursor, query, verbose)  # run query

        if rowCount:
            if verbose:
                print "\n*** Table: %s" % table

            columnNames = selection.replace(", ", ";")
            outFile.write("%s;%s\n" % (table, columnNames))

            selection = selection.replace(" ", "").split(",")

            for row in result:
                i = 0
                values = ""

                for columnName in selection:
                    column = row[i]
                    values = "%s;%s" % (values, column)

                    if verbose:
                        print "    %s: %s" % (columnName, column)

                    i += 1

                outFile.write("%s\n" % values)

                if verbose:
                    print

    if verbose:
        print "\n*** Closing file %s ..." % outFilePath
    outFile.close()

    if verbose:
        print "\n*** Moving file \n    %s \n    to \n    %s" % (outFilePath, USBPath)

    copy(outFilePath, USBPath)
    filesWritten += 1

    # log files
    dirName, fileName, extension = splitPath(logFile, verbose)

    logFileName = os.path.join(USBPath, "%s-%s.%s" % (fileName, timeStamp, extension))

    if verbose:
        print "\n*** Copying \n    %s \n    to \n    %s ..." % (logFile, logFileName)

    copyfile(logFile, logFileName)
    filesWritten += 1

    if verbose:
        print "    %s" % gpioWatchLog

    dirName, fileName, extension = splitPath(gpioWatchLog, verbose)

    gpioWatchLogName = os.path.join(
        USBPath, "%s-%s.%s" % (fileName, timeStamp, extension)
    )

    if verbose:
        print "\n*** Copying \n    %s \n    to \n    %s ..." % (
            gpioWatchLog,
            gpioWatchLogName,
        )

    copyfile(gpioWatchLog, gpioWatchLogName)
    filesWritten += 1

    # close cursor
    db_close_cursor(cnx, cursor, verbose)

    # close db
    db_disconnect(cnx, verbose)

    LCDMessage = "%s files written" % filesWritten

    if verbose:
        print "\n*** Printing to LCD: \n    %s" % LCDMessage

    displayOnLCD("", LCDMessage, verbose)


def readFromFile():
    timeNow = datetime.today()
    timeStamp = timeNow.strftime("%Y%m%d%H%M%S")

    USBPath = findUSBMountPoint(USBDir, labelMatch, verbose)
    if not USBPath:
        LCDMessage = "No USB inserted"
        if verbose:
            print "\n*** Printing to LCD: \n    %s" % LCDMessage
        displayOnLCD("", LCDMessage, verbose)
        onError(4, "No matching USB mounted")
    else:
        displayOnLCD("", "Reading files...", verbose)

    if verbose:
        print "\n*** Searching for files in %s ..." % USBDir

    foundFiles = []
    for f in os.listdir(USBPath):
        if f.startswith("piSchoolBellDb-") and f.endswith(".csv"):
            foundFiles.append(os.path.join(USBPath, f))

    if foundFiles:
        if verbose:
            print "    %s files found:" % len(foundFiles)
            for f in foundFiles:
                print "    %s" % f

        foundFiles = sorted(foundFiles, reverse=True)
        inFile = foundFiles[0]

        if verbose:
            print "\n*** %s\n    is the latest" % inFile

        rowsInserted, rowsUpdated = importToDb(
            inFile, verbose
        )  # import from file to database

        if rowsInserted:
            if verbose:
                print "\n*** %s rows inserted" % rowsInserted
        else:
            if verbose:
                print "\n*** Nothing inserted"

        if rowsUpdated:
            if verbose:
                print "\n*** %s rows updated" % rowsUpdated
        else:
            if verbose:
                print "\n*** Nothing updated"

        displayOnLCD("", "%s rows inserted" % rowsInserted, verbose)

    else:
        if verbose:
            print "*** No file found"

        displayOnLCD("", "No file found", verbose)

        sys.exit(0)


def importToDb(inFile, verbose):
    valuesInserted = 0
    valuesUpdated = 0

    # connect to database
    cnx = db_connect(verbose)

    # create cursor
    cursor = db_create_cursor(cnx, verbose)

    # open file
    if verbose:
        print "\n*** Opening file: \n    %s" % inFile
    with open(inFile) as f:
        content = f.readlines()
    content = [x.strip() for x in content]  # remove unwanted \n and so on

    # iterate through file
    lineNumber = 0

    for line in content:
        lineNumber += 1
        isHeaderLine = False

        oldVerbose = verbose
        # verbose = False
        if verbose:
            print "Line %s: %s" % (lineNumber, line)

        for table in ("breaks", "ringTimes", "ringPatterns", "days"):
            if line.startswith(table):
                thisTable = table
                if verbose:
                    print "\n*** Now processing table: %s" % thisTable
                isHeaderLine = True
                break

        if not isHeaderLine:
            valuesInserted += 1

            values = line.split(";")

            selection = ", %s" % tableSelection(thisTable, verbose)
            selection = selection.replace(" ", "").split(",")

            i = 0
            for column in selection:
                if i != 0:
                    if verbose:
                        print "    %s: %s" % (column, values[i])
                    if i == 1 and values[i]:
                        print "This should be updated"
                    elif i == 1:
                        print "This should be added"
                i += 1

        verbose = oldVerbose

    if verbose:
        print "\n*** %s rows parsed" % lineNumber

    # close cursor
    db_close_cursor(cnx, cursor, verbose)

    # close db
    db_disconnect(cnx, verbose)

    return valuesInserted, valuesUpdated


if __name__ == "__main__":
    if dump:
        dumpToFile()
    elif read:
        readFromFile()
