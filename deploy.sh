# start containers
# first time
$ docker-compose -f docker-compose.yml up -d

# changes
$ docker-compose -f docker-compose.yml up -d --build

# docker clear docker logs
$ sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' <id_container>)

# docker clear all
docker system prune -a

# get json file credentials from (https://console.cloud.google.com/)
file: auth/credencials-nfc.json


# Create env and run locally (from folder project ex: ~/cs/projects/nfc-scheduler/ )
$ sudo apt-get update
$ sudo apt install python3-venv
$ sudo apt install python3-pip
$ python3 -m venv env
$ source env/bin/activate
$ pip3 install -r services/flask/requirements.txt

# run locally (from folder services/flask/app)
$ export FLASK_APP=app.py
$ python3 app.py

# run main.py (no flask)
$ python3 main.py

# scp local to remote (copy credentials)
$ scp -r auth/ remote_username@10.10.0.2:/home/ubuntu/app/nfc-scheduler/services/flask/app
