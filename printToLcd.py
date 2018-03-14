#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import getopt, sys, time, os

import netifaces as ni

from datetime import datetime

from modules import (db_connect, db_create_cursor, db_close_cursor, db_disconnect, db_query,
                     initialize_lcd, print_to_LCD, nextRing, internet_on, testAddress, 
                     button1Gpio, button2Gpio, 
                     remove_leading_zero, getUptime, minUptime, ipWaitTime,
                     onError, usage)

try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 '1:2:'
                                 'g:'
                                 'vh',
                                 ['line1=', 'line2=', 'gpio=', 'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))
    
# if len(sys.argv) == 1:  # no options passed
#    onError(2, 2)
    
line_1 = ""
line_2 = ""
button1 = False
button2 = False
gpio = False
verbose = False
    
for option, argument in myopts:     
    if option in ('-1', '--line1'):  # first line of LCD
        line_1 = argument
    elif option in ('-2', '--line2'):  # second line of LCD
        line_2 = argument
    elif option in ('-g', '--gpio'):  # button 11 - light LCD
        gpio = argument
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)

if verbose:
    i = 1
    print "\n*** Script run with:"
    for option, argument in myopts:     
        print "        Option %s: %s" % (i, option)
        print "        Argument %s: %s" % (i, argument)
        i += 1

# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx)

# buttons
if gpio:
    if verbose:
        print
    if gpio == button1Gpio:
        button1 = True
        if verbose:
            print "*** Button 1 pressed, pin %s" % gpio
    elif gpio == button2Gpio:
        button2 = True
        if verbose:
            print "*** Button 2 pressed, pin %s" % gpio
    else:
        onError(3, "No action for gpio %s" % gpio)

# wake up LCD
lcd, lcd_wake_time, lcd_columns = initialize_lcd(verbose)  # load lcd
lcd.clear()  # clear screen

# displaying ip on lcd
if button1:
    # find this devices ip address
    interfaceIPs = []
    if verbose:
        print "\n*** Finding interfaces..."
    interfaces = ni.interfaces()
    if verbose:
        print "    Found %s interfaces" % len(interfaces)
        print "\n*** Looking up ip addresses..."
        
    i = 0    
    for interface in interfaces:
        ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
        interfaceIPs.append({"interface%s" % i: interface, "ip%s" % i: ip})
        i += 1
        
    i = 0
    for interfaceIP in interfaceIPs:
        if verbose:
            print "    Interface: %s" % interfaceIP['interface%s' % i]
            print "    IP: %s" % interfaceIP['ip%s' % i]
        if not interfaceIP['ip%s' % i].startswith('127') and not interfaceIP['ip%s' % i].startswith('169'):
            line_2 = interfaceIP['ip%s' % i]
            if verbose:
                print "*** This is the one we will display"
        if verbose:
            print
        i += 1
        
# get current time
dateTimeNow = datetime.now()
timeNow = dateTimeNow.strftime('%H:%M')
dateNow = str(dateTimeNow.strftime('%Y-%m-%d'))

if not line_1:
    time = dateTimeNow.strftime('%H:%M')
    day = remove_leading_zero(dateTimeNow.strftime('%d'))
    month = remove_leading_zero(dateTimeNow.strftime('%m'))
    year = dateTimeNow.strftime('%Y')
    line_1 = "%s %s/%s %s" % (time, day, month, year)
if not line_2:    
    nextRingDay, nextRingDate, nextRingTime, ringTimeName, ringPatternName, ringPattern = nextRing(cursor, dateNow, timeNow, verbose)
    day = remove_leading_zero(nextRingDate.strftime('%d'))
    month = remove_leading_zero(nextRingDate.strftime('%m'))
    year = nextRingDate.strftime('%Y')
    line_2 = "%s %s/%s %s" % (nextRingTime, day, month, year)
    
# print to LCD
print_to_LCD(lcd, 0, 0, "1", line_1, lcd_columns, verbose)
print_to_LCD(lcd, 0, 1, "2", line_2, lcd_columns, verbose)

# close cursor
db_close_cursor(cnx, cursor, verbose)

# close db
db_disconnect(cnx, verbose)

