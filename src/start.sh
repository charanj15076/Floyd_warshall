# This shell scripts requires Python 3.9+ and Node with NPM installed

# install python requirements
pip install -r requirements.txt

# install ionic 
npm install -g @ionic/cli
npm install -g @angular/cli

# setup dbs
python ./api/init_db.py

# start python backend
nohup python3 ./src/api/run.py > logs/api.log.txt 2>&1 &
