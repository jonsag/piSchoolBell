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
    
dayNumberNow = int(datetime.strptime(dateNow, '%Y-%m-%d').strftime('%w')) - 1
if dayNumberNow == -1:
    dayNumberNow = 6
    

print "+++ Date: %s \n    Time: %s \n    Day number: %s" % (dateNow, timeNow, dayNumberNow)

print """
 

 
</body>

</html>
"""