#!/bin/bash

# Die on any errors
set -e

clear


if [[ `whoami` != "root" ]]
then
  printf "\n\n Script must be run as root. \n\n"
  exit 1
fi

printf "\n\n Installing real-time-clock ...\n"
#echo "rtc-ds1307" >> /etc/modules
#sed -i '/exit 0/i echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device\nhwclock -s' /etc/rc.local
sed -i '/exit 0/i /sbin/hwclock -s' /etc/rc.local
echo "dtoverlay=i2c-rtc,ds3231" >> /boot/config.txt
echo "HWCLOCKACCESS=no" >> /etc/default/hwclock
apt-get purge fake-hwclock -y
update-rc.d -f fake-hwclock remove
