# piSchoolBell

This runs a Raspberry Pi as a controller for a school bell.  
It makes the school bell ring at the right times taking the calendar into consideration.  
Also there is an LCD screen to visualize time, database stats, upcoming rings etc.  

Administration of the school bell is done via a web UI.  

It is written entirely in python.  

Also it installs gpio-watch to catch the buttons connected to the Pi's GPIO. [https://github.com/larsks/gpio-watch](https://github.com/larsks/gpio-watch)  

## Updates

### 3/7 -22

Now running on RaspberryPiOS Bullseye.  
Everything updated to run on python3.  
Updated install script.  
Made it easier for those not having the Swedish holidays. (More work needed...)  
New module for printing to LCD.  
Fixed apache not defaulting to index.py.  

### 30/6 -22

The API for Swedish holidays, api.dryg.net, is dead.  
Substituted by [sholiday.faboul.se](https://sholiday.faboul.se/dagar/).  

### 7/3 -20

Changed all GPIO pins to make an easier PCB layout possible.  
This makes all older electric installs incompatible.  
Added KiCad files for new pin layout.  

Corrected editing of ring times.  

### 6/3 -20

Bug discovered  
There was a fault in the database setup.  
Instead of updating, you can:  
Log in to database  
>$ sudo mysql -u root -p piSchoolBell  

Change column type  
>MariaDB [piSchoolBell]> ALTER TABLE ringTimes CHANGE weekDays weekDays VARCHAR(7);  

## Hardware setup

### Parts list

* 1 x Raspberry Pi 3 B+, kjell.com Art#88100 (could be any of the later models)  
* 1 x LCD display, kjell.com Art#90215 (16x2 characters, based on the HD44780 chip)  
* 1 x USB micro power adapter, kjell.com Art#88525  
* 1 x Micro SD card, kjell.com Art#97600  
* 1 x 10k potentiometer, kjell.com Art#90633  
* 1 x 5V relay module, kjell.com Art#87878  
* 4 x Push button, kjell.com Art#36023  
* 4 x 10k resistor  
* 4 x 1k resistor  
* 1 x Switch, kjell.com Art#36016  
* 1 x Casing for rpi, kjell.com Art#89030  
* 1 x Casing for relay, kjell.com Art#89014  
* 1 x RTC-module, kjell.com Art#87984  
* 1 x CR2032 battery, kjell.com ART#33715  
* GPIO header connector, kjell.com Art#87915 (or breakout board)  
* Wiring, cables  
* PCB board, kjell.com Art#89416 or Art#89435 (or a breadboard, just to set it up)  

* Soldering material  

### The build  

Assemble all the parts according to the KiCad files.  

### Install and configure OS

Download RaspberryPiOS Lite from [https://www.raspberrypi.com/software/operating-systems/](https://www.raspberrypi.com/software/operating-systems/).  

Cd to where your download is.  
>$ xz -d 2022-04-04-raspios-bullseye-armhf-lite.img.xz  

Insert SD-card and find out drive letter.  
>$ dmesg  

For example '/dev/mmcblk0' or '/dev/sdb'.  

Unmount if mounted.  
>$ umount /dev/mmcblk0p1  
>$ umount /dev/mmcblk0p2  

Write image to SD-card.  
>$ sudo dd bs=4M if=2022-04-04-raspios-bullseye-armhf-lite.img of=/dev/mmcblk0 conv=fsync status=progress  

Remove SD-card and insert it again to make new partitions visible.  

Mount the first partition.  
>$ sudo mount /dev/mmcblk0p1 /mnt/tmp  

Write empty file to boot partition to enable ssh at boot.  
>$ sudo touch /mnt/tmp/ssh  

Unmount.  
>$ sudo umount /mnt/tmp  

Remove SD-card and insert it in a RPi connected to your local network and boot it up.  

### RPi configuration

For this version of the operating system you should have a monitor and keyboard hooked up at the first boot.  

After some restarts you will start to configure your machine:

* Select keyboard layout  
* Create user and set password. For the sake of this installation it's preferred you set 'pi' as username.  

After this you will have a prompt.  
Find out the ip of the RPi

>$ ifconfig

Connect to the RPi via ssh on another machine (if you don't want to continue as before).  

>$ ssh -ip from above-  -l pi  

Login with the username and password you created earlier  

### Configure

>$ sudo raspi-config  

1 S1    Configure wifi  
2 S4    Change hostname  
4 P2    Set GPU memory to 16  
5 L1    Set locales  
5 L2    Set time zone  
6 A1    Expand file system to use whole SD-card  

Reboot to set new options.  

### Update OS

Connect again  

>$ sudo apt-get update && sudo apt-get upgrade  

## Installation

### Install git

>$ sudo apt-get install git  

### Clone repository

>$ cd /home/pi  
>$ git clone <https://github.com/jonsag/piSchoolBell.git>  

### Run install script

>$ cd /home/pi/piSchoolBell  
>$ sudo ./install.sh  

### Initialize mysql (mariadb)

>$ sudo mysql_secure_installation  

Set root password, and press 'enter' on all other questions

### Create database

>$ sudo /home/pi/piSchoolBell/mysql-setup.sh  

### Add test data, if wanted (otherwise some things will act funny until you create your own entries)  

>$ /home/pi/piSchoolBell/insertTestData.sh  

### Download (Swedish) dates

>$ /home/pi/bin/piSchoolBell/getCalendar.py -v  

### For those living outside of Sweden

If you're not lucky enough to live in Sweden, you can run this to make all weekdays workdays.  

>$ /home/pi/piSchoolBell/makeAllWeekdaysToWorkdays.sh

This includes ALL Mondays to Fridays.  

You will have to manually add your own work free weekdays.  

To set 4'th of July 2023 to work free day (if it wasn't a Sunday already...)  
Connect to mysql  

>$ mysql -u pi -p$(grep password /home/pi/bin/piSchoolBell/mysql-config.ini | awk '{ print $3 }') piSchoolBell
>
>MariaDB [piSchoolBell]> UPDATE days SET isWorkDay = '0' WHERE date = '2023-06-04';

#### Note

In Sweden we use the correct way for dates and numbering days.  

The first day of the week is Monday. It has number '0' in the database.  
When printing dates we use 'YYYY-MM-DD'.  

### Make web pages secure

>$ sudo /home/pi/piSchoolBell/www-secure-setup.sh  

## If you're adding an RTC module

### Enable i2c

>$ sudo raspi-config  

3 I5    Enable I2C interface  

>$ ./install-rtc.sh  

### Set hardware clock

Check that time and date is correct  

>$ date  

Set hardware clock  

>$ sudo hwclock -w  

Comment out the following lines in /lib/udev/hwclock-set  

    if [ -e /run/systemd/system ] ; then  
        exit 0  
    fi  

Reboot  

## Configuration

Press button on unit to display its IP-address on the second line of the LCD.  
Connect to the unit by pointing your browser to  

    http://\<IP-address\>:8080'.  

Edit or add breaks, ring times and ring patterns.  

Remember, you can't really add rings on saturdays or sundays, as this is mainly intended for use on normal school schedules.  

### Automatic tasks

At the first of every month cron will download calendar from 'dryg.net', adding data to the database.  
Every night cron will delete past breaks and days from the database.  

## Usage

Normally the LCD display shows:  
Line 1: HH:MM YYYY-mm-dd, current time and date  
Line 2: HH:MM YYYY-mm-dd, the time and date for the next bell ring  

By pressing button 1, display will show:  
&nbsp;&nbsp;&nbsp;&nbsp;Line 1: days left in db, last date in db  
&nbsp;&nbsp;&nbsp;&nbsp;Line 2: IP-address  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If it shows 'Not connected' it has not been able to acquire an IP address.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The first character on line 2 shows if the unit can access internet.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If it is a '*' it is connected.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If it is a '-' it is not connected.  

Pressing button 2 will make the LCD go back to showing default info.  

## USE THE BELOW WITH CAUTION, NOT TESTED ENOUGH

To dump database and logs to USB-stick:  
Format a stick to fat32 and label it 'PISCHOOLBEL'.  
Insert into Pi.  
&nbsp;&nbsp;&nbsp;&nbsp;Display will show:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The USBs label and drive letter  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'USB mounted'  
Press button 3.  
&nbsp;&nbsp;&nbsp;&nbsp;Display will confirm writing  
&nbsp;&nbsp;&nbsp;&nbsp;When finished display shows number of files written  

Remove USB  
&nbsp;&nbsp;&nbsp;&nbsp;Display will show:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;drive letter  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'USB umounted'  

Edit the database file with the highest date and time on the stick.  
To read back edited file to database:  
Insert the USB-stick.  
&nbsp;&nbsp;&nbsp;&nbsp;Display will show:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The USBs label and drive letter  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'USB mounted'  
Press button 4.  
&nbsp;&nbsp;&nbsp;&nbsp;Display will confirm reading  
&nbsp;&nbsp;&nbsp;&nbsp;...  
Not implemented yet.  
For now it only shows how many lines to read back to the database.  

## Issues

If you get problems with Adafruit_Python_CharLCD failing to write to LCD.  

>$ cd /home/pi/piSchoolBell/Adafruit_Python_CharLCD  
>$ sudo python setup.py install  

## Hardware clock / RTC, quick reference

Check system time:  

>$ date  

Check HW-time:  

>$ sudo hwclock -r  

Set HW-clock to system time:  

>$ sudo hwclock -w  

Set system clock from HW-clock:  

>$ sudo hwclock -s  

Set system date manually:  

>$ date +%Y%m%d -s "20120418"  

Set system time manually:  

>$ date +%T -s "11:14:00"  

Set HW-clock manually:  

>$ sudo hwclock --set --date="2011-08-14 16:45:05"  

## Below is only for my own convenience during programming of this project

>$ rsync -raci ~/Documents/EclipseWorkspace/piSchoolBell/* pi@192.168.10.44:/home/pi/bin/piSchoolBell/  
>$ rsync -raci ~/Documents/EclipseWorkspace/piSchoolBell/www/* pi@192.168.10.44:/var/www/piSchoolBell/  
>$ ssh pi@192.168.10.44 'sudo chmod 755 -R /var/www/piSchoolBell'  
>$ ssh pi@192.168.10.44 'sudo chown -R pi:www-data /var/www/piSchoolBell'  
>$ rsync -raci ~/Documents/EclipseWorkspace/piSchoolBell/purgeDatabase.py pi@192.168.10.44:/home/pi/bin/piSchoolBell/  
>
>$ rsync -raci ~/Documents/CodeWorkspace/piSchoolBell pi@192.168.10.99:/home/pi/  
>$ rsync -raci ~/Documents/CodeWorkspace/piSchoolBell/bin/* pi@192.168.10.99:/home/pi/bin/piSchoolBell  

### Things to check after install

>$ list /home/pi/bin/piSchoolBell/  
>$ cat /home/pi/bin/piSchoolBell/gpio.service  
>$ cat /lib/systemd/system/gpio.service  
>$ list /home/pi/bin/piSchoolBell/gpio-scripts  
>$ cat /home/pi/bin/piSchoolBell/gpio-scripts/gpio-script  
>$ list /var/www/piSchoolBell  
>$ cat etc/cron.d/piSchoolBell  
>$ ps ax | grep gpio  

### Run some tests

>$ /home/pi/bin/piSchoolBell/printToLcd.py -v  
>$ i2cdetect -y 1  
>$ cat /proc/driver/rtc  
