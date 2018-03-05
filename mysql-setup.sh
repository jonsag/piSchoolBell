#!/bin/bash

printf "\n\n\n Please enter the MySQL root password : "
read -s ROOT_PASSWORD

DB_USERNAME='pi'
DB_PASSWORD=$(date | md5sum | head -c12)
DB_SERVER='localhost'
DB_NAME='pi_heating_db'

echo
echo $DB_PASSWORD
echo

mysql -uroot -p$ROOT_PASSWORD<< DATABASE

CREATE DATABASE $DB_NAME CHARACTER SET = utf8;

CREATE USER '$DB_USERNAME'@'$DB_SERVER';
SET PASSWORD FOR '$DB_USERNAME'@'$DB_SERVER' = PASSWORD('$DB_PASSWORD');

GRANT ALL ON $DB_NAME.* TO '$DB_USERNAME'@'$DB_SERVER';

USE $DB_NAME;

CREATE TABLE IF NOT EXISTS devices   (      d_id          int(11)       NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                            name          varchar(256)  NOT NULL,
                                            pin           int(11)       DEFAULT NULL,
                                            active_level  tinyint(4)    DEFAULT NULL,
                                            value         tinyint(1)    DEFAULT 0 );

CREATE TABLE IF NOT EXISTS sensors   (      id            bigint(11)    NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                            ref           varchar(20)   DEFAULT NULL,
                                            name          varchar(256)  DEFAULT NULL,
                                            ip            varchar(16)   DEFAULT NULL,
                                            value         float         DEFAULT NULL,
                                            unit          varchar(11)   NOT NULL );

CREATE TABLE IF NOT EXISTS timers    (      id            int(11)       NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                            name          varchar(256)  DEFAULT NULL,
                                            duration      int(11)       DEFAULT NULL,
                                            value         int(11)       DEFAULT NULL ); 

CREATE TABLE IF NOT EXISTS modes     (      id            int(11)       NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                            name          varchar(256)  DEFAULT NULL,
                                            value         tinyint(1)    DEFAULT NULL );
                                            
CREATE TABLE IF NOT EXISTS network   (      id            int(11)       NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                            mac           varchar(17)   DEFAULT NULL,
                                            name          varchar(256)  DEFAULT NULL,
                                            value         tinyint(1)    DEFAULT NULL );
                            
CREATE TABLE IF NOT EXISTS schedules (      id            int(11)       NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                                            name          varchar(256)  DEFAULT NULL,
                                            start         time DEFAULT  NULL,
                                            end           time DEFAULT  NULL,  
                                            dow1          tinyint(1)    NOT NULL DEFAULT '0',
                                            dow2          tinyint(1)    NOT NULL DEFAULT '0',
                                            dow3          tinyint(1)    NOT NULL DEFAULT '0',
                                            dow4          tinyint(1)    NOT NULL DEFAULT '0',
                                            dow5          tinyint(1)    NOT NULL DEFAULT '0',
                                            dow6          tinyint(1)    NOT NULL DEFAULT '0',
                                            dow7          tinyint(1)    NOT NULL DEFAULT '0',
                                            enabled       tinyint(1)    NOT NULL DEFAULT '1',
                                            active        tinyint(1)    DEFAULT NULL );

CREATE TABLE IF NOT EXISTS sched_device (   sd_id         int(11)       NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                            sched_id      int(11)       DEFAULT NULL,
                                            device_id     int(11)       DEFAULT NULL );

CREATE TABLE IF NOT EXISTS sched_sensor (   ss_id         int(11)       NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                            sched_id      int(11)       DEFAULT NULL,
                                            sensor_id     int(11)       DEFAULT NULL,
                                            opp           char(1)       DEFAULT NULL,
                                            value         float         DEFAULT NULL );

CREATE TABLE IF NOT EXISTS sched_timer (    st_id         int(11)       NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                            sched_id      int(11)       DEFAULT NULL,
                                            timer_id      int(11)       DEFAULT NULL,
                                            opp           char(1)       DEFAULT NULL,
                                            value         tinyint(1)    DEFAULT NULL );

CREATE TABLE IF NOT EXISTS sched_mode (     sm_id         int(11)       NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                            sched_id      int(11)       DEFAULT NULL,
                                            mode_id       int(11)       DEFAULT NULL,
                                            test_opp      char(1)       DEFAULT NULL,
                                            test_value    tinyint(1)    DEFAULT NULL );
                                            
CREATE TABLE IF NOT EXISTS sched_network (  sn_id         int(11)       NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                            sched_id      int(11)       DEFAULT NULL,
                                            network_id    int(11)       DEFAULT NULL,
                                            test          tinyint(1)    DEFAULT NULL );

DATABASE

cat > /home/pi/bin/piSchoolBell/mysql-config.ini <<CONFIG
[db]
server = $DB_SERVER
user = $DB_USERNAME
password = $DB_PASSWORD
database = $DB_NAME
CONFIG
