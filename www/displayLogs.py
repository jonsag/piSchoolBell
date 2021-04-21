#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import cgi
import cgitb

cgitb.enable()  # for troubleshooting

from modules import logFile, webPageFooter

print "Content-type: text/html"
print

print """
<html>

<head><title>piSchoolBell - log files</title></head>
 
<body>
 
<h3> piSchoolBell - log files</h3>
"""


def pageLinks():
    print "\n<br>"
    print '\n<br><a href="displayLogs.py">Reset page</a>'

    print "\n<br>"
    print '\n<br><a href="index.py">Home</a>'

    # print '&emsp;<a href="ringPatterns.py?addRingPattern=1">Add another ring pattern</a>'


def pageBody():
    print "\n<br>"

    for fileName in (logFile, "/home/pi/bin/piSchoolBell/gpio-watch.log"):
        print "\n<br>"
        print "\n<br>File name: %s" % fileName
        print "\n<hr>"

        with open(fileName) as f:
            content = f.readlines()

        content = [x.strip() for x in content]

        if content:
            for line in content:
                print "\n<br>%s" % line
        else:
            print "\n<br>------ No entries in %s -----" % fileName


if __name__ == "__main__":
    pageLinks()
    pageBody()
    pageLinks()
    webPageFooter()


print """
 

 
</body>

</html>
"""