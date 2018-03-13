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
if [[ $OS_VERSION != *"stretch"* ]]
then
  printf "\n\n EXITING : Script must be run on PI OS Stretch. \n\n"
  exit 1
fi


APACHE_INSTALLED=$(which apache2)
if [[ "$APACHE_INSTALLED" == "" ]]
then
  printf "\n\n Installing Apache ...\n"
  # Install Apache
  apt-get install apache2 -y
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
  apt-get install mysql-server -y --fix-missing

  MYSQL_INSTALLED=$(which mysql)
    if [[ "$MYSQL_INSTALLED" == "" ]]
    then
      printf "\n\n EXITING : MYSQL installation FAILED\n"
      exit 1
    fi
else
  printf "\n\n MYSQL is already installed. \n"
fi



PYMYSQL_INSTALLED=$(find /var/lib/dpkg -name python-mysql*)
if [[ "$PYMYSQL_INSTALLED" == "" ]]
then
  printf "\n\n Installing MYSQL Python Module ...\n"
  # Install Apache
  apt-get install python-mysqldb -y

  PYMYSQL_INSTALLED=$(find /var/lib/dpkg -name python-mysql*)
    if [[ "$PYMYSQL_INSTALLED" == "" ]]
    then
      printf "\n\n EXITING : MYSQL Python Module installation FAILED\n"
      exit 1
    fi
else
  printf "\n\n MYSQL Python Module is already installed. \n"
fi

printf "\n\n Installing the rest ...\n"
apt-get install python-dev python-setuptools build-essential python-smbus python-pip

printf "\n\n easy_install ...\n"
easy_install -U distribute

printf "\n\n pip ...\n"
pip install RPi.GPIO python-dateutil netifaces

printf "\n\n Installing other stuff ...\n"
apt-get install emacs screen

printf "\n\n Installing piSchoolBell app ...\n"
mkdir -p /home/pi/bin/piSchoolBell
cp -R config.ini gpio.service gpio-script *.py /home/pi/bin/piSchoolBell/
chown pi:pi -R /home/pi/bin/piSchoolBell

printf "\n\n Installing piSchoolBell www ...\n"
mkdir /var/www/piSchoolBell
cp www/* /var/www/piSchoolBell/
chown -R pi:www-data /var/www/piSchoolBell
ln -s /home/pi/bin/piSchoolBell/config.ini /var/www/piSchoolBell/config.ini
ln -s /home/pi/bin/piSchoolBell/modules.py /var/www/piSchoolBell/modules.py
chmod 755 -R /var/www/piSchoolBell/*.py

printf "\n\n Installing Adafruit_Python_CharLCD ...\n
python /home/pi/piSchoolBell/setup.py install

printf "\n\n Installing Adafruit_Python_CharLCD ...\n
cd /home/pi/piSchoolBell/gpio-watch  
make 
sudo make install

printf "\n\n Installing gpio-watch ...\n
touch /home/pi/bin/piSchoolBell/gpio-watch.log
ln -s /home/pi/bin/piSchoolBell/gpio.service /lib/systemd/system/gpio.service
sudo chmod 644 /lib/systemd/system/gpio.service  
systemctl daemon-reload  
systemctl enable gpio.service  
systemctl start gpio.service

printf "\n\n Installing cron job ...\n"
if [ ! -f "/etc/cron.d/piSchoolBell" ]
  then
    cat > /etc/cron.d/piSchoolBell <<CRON
*/1 * * * * pi /home/pi/bin/piSchoolBell/printToLcd.py >> /dev/null 2>&1
CRON
    service cron restart
  fi


printf "\n\n Set up apache to run cgi ...\n"
a2dismod mpm_event
a2enmod mpm_prefork cgi

# configure app

# configure apache virtual host on port 8080

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
    	ErrorLog ${APACHE_LOG_DIR}/error.log  
        CustomLog ${APACHE_LOG_DIR}/access.log combined  
	</VirtualHost>
VHOST

a2ensite piSchoolBell.conf
service apache2 restart

printf "\n\n Installation Complete. Some changes might require a reboot. \n\n"
exit 1

