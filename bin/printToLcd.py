#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import getopt, sys

import netifaces as ni

from modules import (internetAccess, testAddress, 
                     button1Gpio, button2Gpio, displayOnLCD, 
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

# displaying ip on lcd
def button1Pressed():
    
    # find this devices ip address
    interfaceIPs = []
    line_2 = "Not connected"
    
    if verbose:
        print "\n*** Finding interfaces..."
    interfaces = ni.interfaces()
    if verbose:
        print "    Found %s interfaces" % len(interfaces)
        print "\n*** Looking up ip addresses..."
        
    i = 0    
    for interface in interfaces:
        try:
            ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
        except:
            ip = "NA"
        interfaceIPs.append({"interface%s" % i: interface, "ip%s" % i: ip})
        i += 1
        
    i = 0
    for interfaceIP in interfaceIPs:
        if verbose:
            print "    Interface: %s" % interfaceIP['interface%s' % i]
            print "    IP: %s" % interfaceIP['ip%s' % i]
        if (not interfaceIP['ip%s' % i].startswith('127') 
            and not interfaceIP['ip%s' % i].startswith('169') 
            and not interfaceIP['ip%s' % i] == "NA"
            ):
            line_2 = interfaceIP['ip%s' % i]
            if verbose:
                print "*** This is the one we will display"
        if verbose:
            print
        i += 1
    
    if internetAccess(testAddress, verbose):
        line_2 = "*%s" % line_2
    else:
        line_2 = "-%s" % line_2
        
    return line_2
        

if __name__ == '__main__':
    if button1:
        line_2 = button1Pressed()
    displayOnLCD(line_1, line_2, verbose)
    

