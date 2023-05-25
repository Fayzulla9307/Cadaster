#!/bin/bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
sudo apt-get install nginx
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install mysql-server
sudo apt-get install mysql-client

echo "Would you like to configure MySQL? (Y/N)"
read answer
if [[ "$answer" == "Y" || "$answer" == "y" ]]
then
	echo "CREATE DATABASE IF NOT EXISTS balans;" > reset.sql
	echo "CREATE USER IF NOT EXISTS 'balans'@'localhost' IDENTIFIED BY 'RathowtOjpydedNo';" >> reset.sql
	echo "GRANT ALL PRIVILEGES ON * . * TO 'balans'@'localhost';" >> reset.sql
	echo "FLUSH PRIVILEGES;" >> reset.sql
	#echo "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'RathowtOjpydedNo';" > reset.sql
	sudo mysql -uroot < reset.sql
	rm reset.sql
fi

sudo apt-get install python3-mysqldb

sudo pip3 install flask
sudo pip3 install flask-sqlalchemy
sudo pip3 install pycryptodome

echo "Creating application folder"
sudo mkdir -p /opt/kadastr
sudo chown www-data:www-data -R /opt/kadastr

#echo "Would you like to reset the database? (Y/N)"
#read answer
#if [[ "$answer" == "Y" || "$answer" == "y" ]]
#then
#	mysql -ubalans -pRathowtOjpydedNo < ../database/schema.sql
#fi

sudo rsunc -rv ../nginx/default /etc/ngnix/site-available/kadastr
sudo ln -s /etc/nginx/site-available/kadastr /etc/nginx/sites-enabled/kadastr
sudo service nginx restart

sudo rsync -rv ../backend/app ../backend/run.py ../backend/config.py /opt/kadastr/
sudo chown www-data:www-data -R /opt/kadastr

sudo rsync -rv ../frontend/kadastr/dist/* /var/www/kadastr/

sudo rsync -rv ../systemd/kadastr.service /etc/systemd/system/
sudo systemctl enable kadastr
sudo systemctl start kadastr


sudo certbot --nginx -d kadastr.uzgeolcom.uz
