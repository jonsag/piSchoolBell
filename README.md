# piSchoolBell
The goal of this project is to run a Raspberry Pi as a controller for a school bell. It will make the school bell ring at the right times taking the calendar into consideration. Also there will be a LCD screen to visualize some things.  

Administration of the school bell is done via a web page.  

Installing OS
=============================
Download Raspbian Stretch Lite from https://www.raspberrypi.org/downloads/raspbian/  
Choose the Light zip-file  

Cd to where your download is  
$ unzip 2017-11-29-raspbian-stretch-lite.zip  

Insert SD-card and find out drive letter  
$ dmesg  
For example /dev/mmcblk0 or /dev/sdb  

Unmount if mounted  
$ umount /dev/mmcblk0p1  
$ umount /dev/mmcblk0p2  

Write image to SD-card  
$ sudo dd bs=4M if=2017-11-29-raspbian-stretch-lite.img of=/dev/mmcblk0 conv=fsync status=progress 

Remove SD-card and insert it again to make new partitons visible     

Mount the first partition  
$ sudo mount /dev/mmcblk0p1 /mnt/tmp  

Write empty file to boot partition to enable ssh at boot  
$ sudo touch /mnt/tmp/ssh  

Unmount  
$ sudo umount /mnt/tmp  

Remove SD-card and insert it a Rpi connected to your local network and boot it up 

Rpi configuration
-----------------------------
Connect to Rpi via ssh  
Login with user: pi and password:raspberry   

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
Reboot to set new options  

Update
-----------------------------
Connect again  
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
Use the same password as pi login  
Quit with exit  

Create database
-----------------------------
$ sudo /home/pi/piSchoolBell/mysql-setup.sh  

Make web pages secure
-----------------------------
$ sudo /home/pi/piSchoolBell/www-secure-setup.sh  

Download dates
-----------------------------
/home/pi/bin/piSchoolBell/getCalendar.py -v  

Add test data, if wanted (otherwise some things will act funny until you create your own entries)  
-----------------------------
$ sudo mysql -u root -p piSchoolBell < mysql-test-data.sql  

Configuration
=============================
Press button on unit to display its IP-address on the second line of the LCD  
Connect to the unit by pointing your browser to http://<IP-address>:8080  
Edit or add breaks, ring times and ring patterns  

At the first of every month cron will download calendar from dryg.net, adding data to the database  
Every night cron will delete past breaks and days from the database  
Each of these events will be written to the logfile at /home/pi/bin/piSChoolBell/piSchoolBell.log  

Issues
=============================
If you get problems with Adafruit_CharLCD failing to write to LCD
$ cd /home/pi/piSchoolBell/Adafruit_CharLCD
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













