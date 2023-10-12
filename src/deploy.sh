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
#	- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO
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