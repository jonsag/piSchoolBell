# piSchoolBell
The goal of this project is to run a Raspberry Pi as a controller for a school bell. It will make the school bell ring at the right times taking the calendar into consideration. Also there will be a LCD screen to visualize some things.

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

Update  
$ sudo apt-get update && sudo apt-get upgrade  

Configure  
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

Installation
=============================
Later i will probably make an installation script, but for now this is how it goes...  

Install prerequisites
-----------------------------
$ sudo apt-get install git python-dev python-setuptools build-essential python-smbus python-pip mysql-server python-mysqldb apache2  

$ sudo easy_install -U distribute  
$ sudo pip install RPi.GPIO python-dateutil  

Initialize mysql
-----------------------------
$ sudo mysql -u root -p  
Use the same password as pi login  
Quit with exit  

Set up apache to run python
-----------------------------
$ sudo a2dismod mpm_event  
$ sudo a2enmod mpm_prefork cgi  

$ sudo echo "Listen 8080" >> /etc/apache2/ports.conf  

Edit /etc/apache2/sites-avalable/piSchoolBell.conf  
	<VirtualHost *:8080>  
    	ServerAdmin webmaster@localhost  
    	DocumentRoot /var/www/piSchoolBell/  
    	<Directory /var/www/piSchoolBell/>  
        	Options -Indexes  
        	AllowOverride all  
        	Order allow,deny  
        	allow from all  
    	</Directory>  
    	<Directory /var/www/piSchoolBell/cgi-bin/>  
        	Options +ExecCGI  
        	AddHandler cgi-script .py  
    	</Directory>  
    	ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
	</VirtualHost>  
	
$ sudo a2ensite piSchoolBell.conf  
$ sudo systemctl restart apache2  

Install other useful stuff
-----------------------------
$ sudo apt-get install emacs screen  

Clone repository
-----------------------------
$ cd /home/pi  
$ git clone https://github.com/jonsag/piSchoolBell.git  

$ cd /home/pi/piSchoolBell  

Create database and insert initial data
-----------------------------
$ sudo ./mysql-setup.sh  

Add test data, if wanted  
$ sudo mysql -u root -p piSchoolBell < mysql-test-data.sql  

Create directories and copy files
-----------------------------
$ mkdir -p /home/pi/bin/piSchoolBell  
$ cp config.ini gpio.service gpio-script *.py /home/pi/bin/piSchoolBell/
$ sudo mkdir /var/www/piSchoolBell  
$ cp www /var/www/piSchoolBell
$ sudo chown -R pi:www-data /var/www/piSchoolBell 
$ sudo chmod 755 -R /var/www/piSchoolBell  

Install Adafruit_Python_CharLCD python module by Adafruit from https://github.com/adafruit/Adafruit_Python_CharLCD.git  
-----------------------------
$ cd /home/pi/piSchoolBell/Adafruit_Python_CharLCD  
$ sudo python setup.py install  

Install gpio-watch by larsks from https://github.com/larsks/gpio-watch  
-----------------------------
$ cd /home/pi/piSchoolBell/gpio-watch  
$ make  
$ sudo make install  

Setup gpio-watch
-----------------------------
$ touch /home/pi/bin/piSchoolBell/gpio-watch.log  
  
$ sudo  ln -s /home/pi/bin/piSchoolBell/gpio.service /lib/systemd/system/gpio.service  
$ sudo chmod 644 /lib/systemd/system/gpio.service  
$ sudo systemctl daemon-reload  
$ sudo systemctl enable gpio.service  

Setup cron jobs
-----------------------------
$ crontab -e  
	*/1 * * * * /home/pi/bin/piSchoolBell/printToLcd.py >> /dev/null 2>&1  
	




rsync -raci ~/Documents/EclipseWorkspace/piSchoolBell/* pi@192.168.10.44:/home/pi/bin/piSchoolBell/

rsync -raci ~/Documents/EclipseWorkspace/piSchoolBell/www/* pi@192.168.10.44:/var/www/piSchoolBell/
ssh pi@192.168.10.44 'sudo chmod 755 -R /var/www/piSchoolBell'
ssh pi@192.168.10.44 'sudo chown -R pi:www-data /var/www/piSchoolBell'




