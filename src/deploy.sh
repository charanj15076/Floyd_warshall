########### DEPLOYMENT INFO ###########

## STEP 1 Set up environment

# - Apt install python3, python3-pip, postgresql, postgis, npm, nginx, libgdal-dev
#		- may need to manually install GDAL if it fails: $ pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')
#		- upgrade node to latest npm install -g n stable
# - Create DB
#		$ createdb cpsc535proj2
# - go to $ psql cpsc535proj2 and create python user
# - run: CREATE USER python WITH PASSWORD 'password';
# - run: GRANT ALL PRIVILEGES ON DATABASE cpsc535proj2 TO python; ...do the same with schema, table, sequence...
#	- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO python;
#	- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO python;
# - restart nginx and postgres: sudo systemctl start nginx, sudo service postgresql restart
# 		- remove default sites-enabled and sites-available

## STEP 2: create .env file

## STEP 3: run start.sh

## STEP 4: build front end
# -- development 
# cd app
# ionic serve > ../logs/app.log.txt 2>&1 &
#
# -- prod
# npm run build



## STEP 5: deploy the ionic app (cordova for desktop, capacitor for mobile)
# (for browser)
# $ ionic integrations disable capacitor  		#### temporarily disables capacitor
# $ npm i -g cordova     						#### install cordova
# $ ionic cordova platform add browser
# $ ionic build --prod  
# - a www directory will show up and you can upload it to the hosting service (EC2 for our case)
#  tar -czvf www.tar.gz www/   
# .ssh % scp -i ken-keypair.pem -r ./src/app/www.tar.gz ubuntu@ec2-34-219-32-158.us-west-2.compute.amazonaws.com:/home/ubuntu
# - on the deployed server, configure nginx
# tar -xzvf www.tar.gz 
# sudo mv -f www/* /var/www/html/
# sudo systemctl restart nginx
# - check nginx.application.conf for sites enabled configuration
# sudo ln -s /etc/nginx/sites-available/application.conf /etc/nginx/sites-enabled/application.conf