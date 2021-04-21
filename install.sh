 0 * * * pi /home/pi/bin/piSchoolBell/purgeDatabase.py -c >> /dev/null 2>&1

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
apt-get install pmount -y

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









