#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import getopt, sys, time

from datetime import datetime, timedelta

from modules import (db_connect, db_create_cursor, db_close_cursor, db_disconnect, db_query,
                     initialize_lcd, print_to_LCD,
                     remove_leading_zero, random_chars,
                     active_schedules, active_devices, process_schedules,
                     onError, usage)

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
    if option in ('-l', '--light'):  # turn backlight on
        light = True
    elif option in ('-1', '--line1'):  # first line of LCD
        light = True
        line_1 = argument
    elif option in ('-2', '--line2'):  # second line of LCD
        light = True
        line_2 = argument
    elif option in ('-g', '--gpio'):  # button 11 - light LCD
        light = True
        gpio = argument
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)

if verbose:
    i = 1
    print "\n+++ Script run with:"
    for option, argument in myopts:     
        print "        Option %s: %s" % (i, option)
        print "        Argument %s: %s" % (i, argument)
        i += 1

# connect to database
cnx = db_connect(verbose)

# buttons
if gpio:
    if verbose:
        print
    if gpio == "11":
        if verbose:
            print "+++ Button 1 pressed, pin %s" % gpio
    elif gpio == "25":
        toggleMode = True
        if verbose:
            print "+++ Button 2 pressed, pin %s" % gpio
    elif gpio == "7":
        toggleTimer = True
        if verbose:
            print "+++ Button 3 pressed, pin %s" % gpio
    elif gpio == "8":
        stopModeTimer = True
        if verbose:
            print "+++ Button 4 pressed, pin %s" % gpio
    else:
        onError(3, "No action for gpio %s" % gpio)
            
# what to write to lcd
t = u"\u00b0"  # degree sign
inf = u"\u221e"  # infinity symbol

if not line_1:
    day = remove_leading_zero(timeNow.strftime('%d'))
    month = remove_leading_zero(timeNow.strftime('%m'))
    hour = timeNow.strftime('%H')
    minute = timeNow.strftime('%M')
    line_1 = "%s/%s %s:%s %s%s" % (day, month, hour, minute, temp_value, t)
if not line_2:    
    if mode_value:
        line_2 = "%s%s %s" % (int(activeNow[0]['setPoint']), t, inf)
    elif timer_value != 0:
        line_2 = "%s%s @%s" % (int(activeNow[0]['setPoint']), t, timerEnd)
    else:
        line_2 = "%s%s %s" % (int(activeNow[0]['setPoint']), t, inf)
    #    #line_2 = random_chars()
    #    line_2 = str(temp_value)

# print to lcd
if light:
    lcd, lcd_wake_time, lcd_columns = initialize_lcd(verbose)  # load lcd
    
    # clear screen and turn backlight on
    lcd.clear()
    lcd.set_backlight(1)
    if verbose:
        print "\n--- Backlight ON"
    
    # print to LCD
    print_to_LCD(lcd, 0, 0, "1", line_1, lcd_columns, verbose)
    print_to_LCD(lcd, 0, 1, "2", line_2, lcd_columns, verbose)

    if verbose:
        print "\n--- Wait %ss..." % lcd_wake_time
    time.sleep(lcd_wake_time)
        
    # clear screen and turn backlight off.
    lcd.clear()
    lcd.set_backlight(0)
    if verbose:
        print "\n--- Backlight OFF"
        
if verbose:
    print "\n+++ Active schedules:"
    active_schedules(cursor, cnx, verbose)
    print "\n+++ Active devices:"
    active_devices(cursor, cnx, verbose)

# close db
db_disconnect(cnx, verbose)

