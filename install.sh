#!/bin/bash

# Die on any errors
#set -e

clear


if [[ `whoami` != "root" ]]
then
    printf "\n\n Script must be run as root. \n\n"
    exit 1
fi


OS_VERSION=$(cat /etc/os-release | grep VERSION=)
if [[ $OS_VERSION != *"bullseye"* ]]
then
    printf "\n\n EXITING : Script must be run on PI OS Stretch. \n\n"
    exit 1
fi


APACHE_INSTALLED=$(which apache2)
if [[ "$APACHE_INSTALLED" == "" ]]
then
    printf "\n\n Installing Apache ...\n"
    # Install Apache
    apt install apache2 -y
    update-rc.d apache2 enable
    a2dissite 000-default.conf
    service apache2 restart
    
    APACHE_INSTALLED=$(which apache2)
    if [[ "$APACHE_INSTALLED" == "" ]]
    then
        printf "\n\n EXITING : Apache installation FAILED\n"
        exit 1
    fi
else
    printf "\n\n Apache is already installed. \n"
fi


MYSQL_INSTALLED=$(which mysql)
if [[ "$MYSQL_INSTALLED" == "" ]]
then
    printf "\n\n Installing MYSQL ...\n"
    # Install Apache
    apt install mariadb-server -y --fix-missing
    
    MYSQL_INSTALLED=$(which mysql)
    if [[ "$MYSQL_INSTALLED" == "" ]]
    then
        printf "\n\n EXITING : MYSQL installation FAILED\n"
        exit 1
    fi
else
    printf "\n\n MYSQL is already installed. \n"
fi


PYMYSQL_INSTALLED=$(find /var/lib/dpkg -name python3-mysql*)
if [[ "$PYMYSQL_INSTALLED" == "" ]]
then
    printf "\n\n Installing MYSQL Python Module ...\n"
    # Install Apache
    apt install python3-mysqldb -y
    
    PYMYSQL_INSTALLED=$(find /var/lib/dpkg -name python3-mysql*)
    if [[ "$PYMYSQL_INSTALLED" == "" ]]
    then
        printf "\n\n EXITING : MYSQL Python Module installation FAILED\n"
        exit 1
    fi
else
    printf "\n\n MYSQL Python Module is already installed. \n"
fi


printf "\n\n Installing the rest ...\n"
apt install python3-dev python3-setuptools build-essential python3-smbus python3-pip python3-netifaces python3-dateutil python3-rpi.gpio at -y


#printf "\n\n easy_install ...\n"
#easy_install -U distribute


printf "\n\n pip ...\n"
pip install adafruit-circuitpython-charlcd #distribute


#printf "\n\n Installing Adafruit_Python_CharLCD ...\n"
#python /home/pi/piSchoolBell/Adafruit_Python_CharLCD/setup.py install


printf "\n\n Installing other stuff ...\n"
apt install emacs-nox screen locate -y


printf "\n\n Installing piSchoolBell app ...\n"
mkdir -p /home/pi/bin/piSchoolBell/tmp
cp -r /home/pi/piSchoolBell/bin/* /home/pi/bin/piSchoolBell/
ln -s printToLcdGpioScript /home/pi/bin/piSchoolBell/gpio-scripts/7
ln -s printToLcdGpioScript /home/pi/bin/piSchoolBell/gpio-scripts/8
ln -s databaseReadWriteGpioScript /home/pi/bin/piSchoolBell/gpio-scripts/9
ln -s databaseReadWriteGpioScript /home/pi/bin/piSchoolBell/gpio-scripts/10
touch /home/pi/bin/piSchoolBell/piSchoolBell.log
chown pi:pi -R /home/pi/bin


printf "\n\n Installing piSchoolBell www ...\n"
mkdir /var/www/piSchoolBell
cp /home/pi/piSchoolBell/www/* /var/www/piSchoolBell/
chown -R pi:www-data /var/www/piSchoolBell
ln -s /home/pi/bin/piSchoolBell/config.ini /var/www/piSchoolBell/config.ini
ln -s /home/pi/bin/piSchoolBell/modules.py /var/www/piSchoolBell/modules.py
chmod 755 -R /var/www/piSchoolBell/*.py


printf "\n\n Installing gpio-watch ...\n"
make --directory /home/pi/piSchoolBell/gpio-watch
make --directory /home/pi/piSchoolBell/gpio-watch install


printf "\n\n Setting up gpio-watch ...\n"
touch /home/pi/bin/piSchoolBell/gpio-watch.log
chown pi:pi /home/pi/bin/piSchoolBell/gpio-watch.log
ln -s /home/pi/bin/piSchoolBell/gpio.service /lib/systemd/system/gpio.service
chmod 644 /lib/systemd/system/gpio.service
systemctl daemon-reload
systemctl enable gpio.service
systemctl start gpio.service


printf "\n\n Installing cron job ...\n"
if [ ! -f "/etc/cron.d/piSchoolBell" ]
then
    cat > /etc/cron.d/piSchoolBell <<CRON
# Print time and next ring to LCD every minute
*/1 * * * * pi /home/pi/bin/piSchoolBell/printToLcd.py >> /dev/null 2>&1

# Check if its time to ring bell
*/1 * * * * pi /home/pi/bin/piSchoolBell/ringBell.py >> /dev/null 2>&

# Get new days at the first of every month
5 0 1 * * pi /home/pi/bin/piSchoolBell/getCalendar.py -c >> /dev/null 2>&1

# Purge database every night
10 0 * * * pi /home/pi/bin/piSchoolBell/purgeDatabase.py -c >> /dev/null 2>&1

CRON
    service cron restart
fi


printf "\n\n Set up apache to run cgi ...\n"
a2dismod mpm_event
a2enmod mpm_prefork cgi


printf "\n\n Configuring Apache ...\n"
  cat >> /etc/apache2/ports.conf <<PORTS
Listen 8080
PORTS

  cat > /etc/apache2/sites-available/piSchoolBell.conf <<VHOST
<VirtualHost *:8080>
    	ServerAdmin webmaster@localhost
    	DocumentRoot /var/www/piSchoolBell/
    	<Directory /var/www/piSchoolBell/>
        	Options -Indexes
        	AllowOverride all
        	Order allow,deny
        	allow from all
        	Options +ExecCGI
        	AddHandler cgi-script .py
    	</Directory>
    	ErrorLog \${APACHE_LOG_DIR}/error.log
        CustomLog \${APACHE_LOG_DIR}/access.log combined
	</VirtualHost>
VHOST

a2ensite piSchoolBell.conf
service apache2 restart


printf "\n\n Setting up USB auto mount ...\n"
apt install pmount -y

ln -s /home/pi/bin/piSchoolBell/usbstick.rules /etc/udev/rules.d/usbstick.rules
udevadm control --reload-rules
#udevadm trigger

ln -s /home/pi/bin/piSchoolBell/usbstick-handler@.service /lib/systemd/system/usbstick-handler@.service
systemctl daemon-reload

ln -s /home/pi/bin/piSchoolBell/automount /usr/local/bin/automount
ln -s /home/pi/bin/piSchoolBell/autoumount /usr/local/bin/autoumount

printf "\n\n Some after adjustments ...\n"
cat >> /home/pi/.bashrc <<ALIAS
alias list='ls -alFh'
ALIAS

cp /root/.bashrc /root/.bashrc.old
cp /home/pi/.bashrc /root/.bashrc



printf "\n\n Installation Complete. Some changes might require a reboot. \n\n"
exit 1
