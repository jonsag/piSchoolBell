#!/bin/bash

# Die on any errors
set -e

clear

if [[ $(whoami) != "root" ]]; then
  printf "\n\n Script must be run as root. \n\n"
  exit 1
fi

printf "\n\n Installing real-time-clock ...\n"
sed -i '/exit 0/i at now + 1 min < /home/pi/bin/piSchoolBell/startRTC.sh' /etc/rc.local

echo "dtoverlay=i2c-rtc,ds3231" >>/boot/config.txt
echo "HWCLOCKACCESS=no" >>/etc/default/hwclock

apt-get purge fake-hwclock -y

update-rc.d -f fake-hwclock remove
