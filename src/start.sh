# This shell scripts requires Python 3.9+ and Node with NPM installed

# install python requirements
pip install -r requirements.txt

# install ionic 
npm install -g @ionic/cli

# setup dbs
python ./api/init_db.py

# start python backend
python3 ./src/api/run.py > logs/api.log.txt 2>&1 &

# start frontend
cd app
ionic serve > ../logs/app.log.txt 2>&1 &