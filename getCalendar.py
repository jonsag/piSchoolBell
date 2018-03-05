#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from modules import (db_connect, db_create_cursor, db_close_cursor, db_disconnect, db_query, 
                     onError, 
                     drygUri, drygPath)

import getopt, sys, json, calendar

from datetime import date
from dateutil.relativedelta import relativedelta
from urlparse import urljoin
from urllib2 import urlopen

try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 'l'
                                 '1:2:'
                                 'g:'
                                 'vh',
                                 ['line1=', 'line2=', 'gpio=', 'light', 'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))
    
if len(sys.argv) == 1:  # no options passed
    onError(2, 2)
    
light = False
line_1 = ""
line_2 = ""
gpio = False
verbose = False
    
for option, argument in myopts:     
    if option in ('-v', '--verbose'):  # turn backlight on
        verbose = True

timeNow = date.today()
dateNow = timeNow.strftime("%Y-%m-%d")
yearNow = timeNow.strftime("%Y")
monthNow = timeNow.strftime("%m")

calendarAddress = urljoin(drygUri, drygPath)

if verbose:
    print "\n+++ Todays date: %s" % dateNow
    print
    print "+++ Calendar source: %s" % calendarAddress
    
# getting calendars for twelve months
# check if connected to internet
connected = True

if connected:
    for i in range(0, 12, 1):
        lookupDate = timeNow + relativedelta(months=i)
        lookupYear = lookupDate.strftime("%Y")
        lookupMonth = lookupDate.strftime("%m")
        
        calendarPath = "%s/%s/%s" % (calendarAddress, lookupYear, lookupMonth)
        
        if verbose:
            print "\n*** Getting calendar data for: %s-%s" % (lookupYear, lookupMonth)
            print "    %s" % calendarPath
            
        calendarData = urlopen(calendarPath).read() # read calendar data
        
        parsedCalendar = json.loads(calendarData) # load json
        
        if verbose:
            print
            print json.dumps(parsedCalendar, indent=4, sort_keys=True)
        
        day = 0
        
        while True:
            try: # does this month have this day
                date = parsedCalendar["dagar"][day]["datum"]
            except:
                break
            
            dayNumber = int(parsedCalendar["dagar"][day]["dag i vecka"]) - 1
            workFreeDay = parsedCalendar["dagar"][day]["arbetsfri dag"]
            
            try: # is this day an eve
                eve = parsedCalendar["dagar"][day]["helgdagsafton"]
            except:
                eve = ""
            
            try: # is this day an eve
                holiday = parsedCalendar["dagar"][day]["helgdag"]
            except:
                holiday = ""

            if verbose:
                print "\n+++ Date: %s, %s" % (date, calendar.day_name[dayNumber])
                if workFreeDay == "Nej":
                    print "    School day"
                if eve:
                    print "    Eve: %s" % eve
                if holiday:
                    print "    Holiday: %s" % holiday
                
            day += 1 # add one day and test it
        
        
        sys.exit()
        







