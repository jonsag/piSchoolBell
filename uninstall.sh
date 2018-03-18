#!/bin/bash

# Die on any errors

#set -e
clear


if [[ `whoami` != "root" ]]
then
  printf "\n\n Script must be run as root. \n\n"
  exit 1
fi


printf "\n\n Disabling gpio-watch ...\n"
systemctl stop gpio.service
systemctl disable gpio.service
rm /lib/systemd/system/gpio.service
systemctl daemon-reload


printf "\n\n Uninstalling piSchoolBell app ...\n"
rm -R /home/pi/bin/piSchoolBell


printf "\n\n Uninstalling piSchoolBell www ...\n"
rm -R /var/www/piSchoolBell


printf "\n\n Removing cron job ...\n
rm /etc/cron.d/piSchoolBell


printf "\n\n Configuring Apache ...\n"
a2dissite piSchoolBell.conf
rm /etc/apache2/sites-available/piSchoolBell.conf
sed -i".bak" '/Listen 8080/d' /etc/apache2/ports.conf
rm /etc/apache2/ports.conf.bak
service apache2 restart


printf "\n\n Disabling USB auto mount ...\n"
rm /etc/udev/rules.d/usbstick.rules
rm /lib/systemd/system/usbstick-handler@.service
systemctl daemon-reload
rm /usr/local/bin/automount


printf "\n\n Uninstallation Complete. Some changes might require a reboot. \n\n"
exit 1




