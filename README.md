# piSchoolBell
This runs a Raspberry Pi as a controller for a school bell.  
It makes the school bell ring at the right times taking the calendar into consideration.  
Also there is an LCD screen to visualize time, database stats, upcoming rings etc.  

Administration of the school bell is done via a web UI.  

It is written entirely in python.  

It makes use of the Adafruit_Python_CharLCD library. (https://github.com/adafruit/Adafruit_Python_CharLCD)  

Also it installs gpio-watch to catch the buttons connected to the Pi's GPIO. (https://github.com/larsks/gpio-watch)  

Hardware setup
=============================

Parts list
-----------------------------
1 x Raspberry Pi 3 B+, kjell.com Art#88100 (could be any of the later models)  
1 x LCD display, kjell.com Art#90215 (16x2 characters, based on the HD44780 chip)  
1 x USB micro power adapter, kjell.com Art#88525  
1 x Micro SD card, kjell.com Art#97600  
1 x 10k potentiometer, kjell.com Art#90633  
1 x 5V relay module, kjell.com Art#87878  
4 x Push button, kjell.com Art#36023  
4 x 10k resistor  
4 x 1k resistor  
1 x Switch, kjell.com Art#36016  
1 x Casing for rpi, kjell.com Art#89030  
1 x Casing for relay, kjell.com Art#89014  
1 x RTC-module, kjell.com Art#87984  
1 x CR2032 battery, kjell.com ART#33715  
GPIO header connector, kjell.com Art#87915 (or breakout board)  
Wiring, cables  
PCB board, kjell.com Art#89416 or Art#89435 (or a breadboard, just to set it up)  
Soldering material  

The build
-----------------------------
Assemble all the parts according to the files and images in the 'Documents' folder.  

Install and configure OS
=============================
Download Raspbian Stretch Lite from 'https://www.raspberrypi.org/downloads/raspbian/'.  
Choose the Light zip-file.  

Cd to where your download is.  
$ unzip 2017-11-29-raspbian-stretch-lite.zip  

Insert SD-card and find out drive letter.  
$ dmesg  
For example '/dev/mmcblk0' or '/dev/sdb'.  

Unmount if mounted.  
$ umount /dev/mmcblk0p1  
$ umount /dev/mmcblk0p2  

Write image to SD-card.  
$ sudo dd bs=4M if=2017-11-29-raspbian-stretch-lite.img of=/dev/mmcblk0 conv=fsync status=progress  

Remove SD-card and insert it again to make new partitons visible.     

Mount the first partition.  
$ sudo mount /dev/mmcblk0p1 /mnt/tmp  

Write empty file to boot partition to enable ssh at boot.  
$ sudo touch /mnt/tmp/ssh  

Unmount.  
$ sudo umount /mnt/tmp  

Remove SD-card and insert it a Rpi connected to your local network and boot it up. 

Rpi configuration
-----------------------------
Connect to Rpi via ssh.  
Login with user: 'pi' and password: 'raspberry'.   

Configure
-----------------------------
$ sudo raspi-config   

1		Change password  
2 N1	Change hostname  
2 N2	Set SSID and passphrase   
4 I1	Set locales  
4 I2	Set time zone  
4 I3	Choose keyboard layout    
4 I4	Set wifi country  
7 A1	Expand file system to use whole SD-card  
7 A3	Set memory split to 16  

Reboot to set new options.  

Update raspbian
-----------------------------
Connect again.  
$ sudo apt-get update && sudo apt-get upgrade  

Installation
============================= 

Install git
-----------------------------
$ sudo apt-get install git  

Clone repository
-----------------------------
$ cd /home/pi  
$ git clone https://github.com/jonsag/piSchoolBell.git  

Run install script
-----------------------------
$ cd /home/pi/piSchoolBell  
$ sudo ./install.sh   

Initialize mysql
-----------------------------
$ sudo mysql -u root -p  
Use the same password as login for user pi.  
Quit with 'exit;'.  

Create database
-----------------------------
$ sudo /home/pi/piSchoolBell/mysql-setup.sh  

Make web pages secure
-----------------------------
$ sudo /home/pi/piSchoolBell/www-secure-setup.sh  

Download dates
-----------------------------
$ /home/pi/bin/piSchoolBell/getCalendar.py -v  

See 'Issues' below if you get problem with this  

Add test data, if wanted (otherwise some things will act funny until you create your own entries)  
-----------------------------
$ sudo mysql -u root -p piSchoolBell < /home/pi/piSchoolBell/mysql-test-data.sql  

Wireless network setup
-----------------------------
Use the raspi-config you used earlier. 

If you are adding the RTC module
=============================

Enable i2c
---------------------------------
$ sudo raspi-config 

5 P5	Enable I2C interface  

$ ./install-rtc.sh  

Set hardware clock
-----------------------------
Check that time and date is correct  
$ date  

Set hardware clock  
$ sudo hwclock -w  

Comment out the following lines in /lib/udev/hwclock-set  
&nbsp;&nbsp;&nbsp;&nbsp;if [ -e /run/systemd/system ] ; then  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;exit 0  
&nbsp;&nbsp;&nbsp;&nbsp;fi 
	
Reboot  

Configuration
=============================
Press button on unit to display its IP-address on the second line of the LCD.  
Connect to the unit by pointing your browser to 'http://IP-address:8080'.  
Edit or add breaks, ring times and ring patterns.  

Automatic tasks
-----------------------------
At the first of every month cron will download calendar from 'dryg.net', adding data to the database.  
Every night cron will delete past breaks and days from the database.  

Usage
=============================
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

Hardware clock / RTC
-----------------------------  
Check system time:  
$ date  
Check HW-time:  
$ sudo hwclock -r  
Set HW-clock to system time:  
$ sudo hwclock -w  
Set system clock from HW-clock:  
$ sudo hwclock -s  

Set system date manually:  
$ date +%Y%m%d -s "20120418"  
Set system time manually:  
$ date +%T -s "11:14:00"  

Set HW-clock manually:  
4 sudo hwclock --set --date="2011-08-14 16:45:05"  

USE THE BELOW WITH CAUTION, NOT TESTED ENOUGH
-----------------------------
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

Issues
=============================
If you get problems with Adafruit_Python_CharLCD failing to write to LCD.  
$ cd /home/pi/piSchoolBell/Adafruit_Python_CharLCD  
$ sudo python setup.py install  
 

Below is only for my own convieniance during programming of this project
=============================
rsync -raci ~/Documents/EclipseWorkspace/piSchoolBell/* pi@192.168.10.44:/home/pi/bin/piSchoolBell/

rsync -raci ~/Documents/EclipseWorkspace/piSchoolBell/www/* pi@192.168.10.44:/var/www/piSchoolBell/
ssh pi@192.168.10.44 'sudo chmod 755 -R /var/www/piSchoolBell'
ssh pi@192.168.10.44 'sudo chown -R pi:www-data /var/www/piSchoolBell'


rsync -raci ~/Documents/EclipseWorkspace/piSchoolBell/purgeDatabase.py pi@192.168.10.44:/home/pi/bin/piSchoolBell/


Things to check after install
-----------------------------
list /home/pi/bin/piSchoolBell/
cat /home/pi/bin/piSchoolBell/gpio.service
cat /lib/systemd/system/gpio.service

list /home/pi/bin/piSchoolBell/gpio-scripts
cat /home/pi/bin/piSchoolBell/gpio-scripts/gpio-script

list /var/www/piSchoolBell

cat etc/cron.d/piSchoolBell

ps ax | grep gpio

Run some tests
-----------------------------
/home/pi/bin/piSchoolBell/printToLcd.py -v

i2cdetect -y 1

cat /proc/driver/rtc















