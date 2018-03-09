#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

from datetime import datetime

print "Content-type: text/html"
print

print """
<html>

<head><title>piSchoolBell</title></head>
 
<body>
 
<h3> piSchoolBell </h3>
"""

# get current time
dateTimeNow = datetime.now()

dateNow = str(dateTimeNow.strftime('%Y-%m-%d'))


timeNow = dateTimeNow.strftime('%H:%M')

weekNumberNow = datetime.strptime(dateNow, '%Y-%m-%d').strftime('%W')
    
dayNumberNow = int(datetime.strptime(dateNow, '%Y-%m-%d').strftime('%w')) - 1
if dayNumberNow == -1:
    dayNumberNow = 6
    
def pageBody():    

    print '<br>\nDate: %s <br>\nTime: %s <br>\nWeek number: %s <br>\nDay number: %s' % (dateNow, timeNow, weekNumberNow, dayNumberNow)
    
    print '<br>\n'
    print '<br>\n<a href="upcomingRings.py">Upcoming rings</a>'
    
    print '<br>\n'
    print '<br>\n<a href="ringRimes.py">Ring times</a>'
    
    print '<br>\n'
    print '<br>\n<a href="breaks.py">Breaks</a>'
    
    print '<br>\n'
    print '<br>\n<a href="extraDays.py">Extra school days</a>'
    
    print '<br>\n'
    print '<br>\n<a href="ringPatterns.py">Ring patterns</a>'


if __name__ == '__main__':
    pageBody()

print """
 

 
</body>

</html>
"""