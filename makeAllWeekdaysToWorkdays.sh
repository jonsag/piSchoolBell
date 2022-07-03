#!/bin/bash

mysql -u pi -p$(grep password /home/pi/bin/piSchoolBell/mysql-config.ini | awk '{ print $3 }') piSchoolBell < /home/pi/piSchoolBell/mysql-weekdays-to-workdays.sql
