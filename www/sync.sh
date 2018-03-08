#!/bin/bash
rsync -raci ~/Documents/EclipseWorkspace/piSchoolBell/www/* pi@192.168.10.44:/var/www/piSchoolBell/
ssh pi@192.168.10.44 'sudo chmod 755 -R /var/www/piSchoolBell'
ssh pi@192.168.10.44 'sudo chown -R pi:www-data /var/www/piSchoolBell'
