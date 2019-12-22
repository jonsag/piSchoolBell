#!/bin/bash

#          Raspberry Pi setup, 'pi-heating-hub' configuration script.
# Author : Jeffrey.Powell ( jffrypwll <at> googlemail <dot> com )
# Date   : Nov 2016

# Die on any errors

#set -e
clear


if [[ `whoami` != "root" ]]
then
  printf "\n\n Script must be run as root. \n\n"
  exit 1
fi


OS_VERSION=$(cat /etc/os-release | grep VERSION=)
if [[ $OS_VERSION != *"stretch"* ]]
then
  printf "\n\n EXITING : Script must be run on PI OS Stretch. \n\n"
  exit 1
fi


cd /home/pi

cat >> /var/www/piSchoolBell/.htaccess <<ACCESS
AuthName "piSchoolBell"
AuthType Basic
AuthUserFile /home/pi/bin/piSchoolBell/.htpasswd
require valid-user

ACCESS

printf "\n\n Enter password for user admin?\n"
htpasswd -c /home/pi/piSchoolBell/.htpasswd admin

mv /home/pi/piSchoolBell/.htpasswd /home/pi/bin/piSchoolBell/.htpasswd
chmod 644 /home/pi/bin/piSchoolBell/.htpasswd

printf "\n\n Installation Complete. \n\n"
exit 1
