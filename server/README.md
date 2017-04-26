# How to deploy the server

## Clone the repository

SSH:

`git clone git@github.com:ESEGroup/IssuesMonitoring.git`

HTTPS:

`git clone https://github.com/ESEGroup/IssuesMonitoring.git`

## Create virtualenv (at server folder)

`virtualenv -p python3 .env`

## Join the virtualenv

`source .env/bin/activate`

**To leave the virtualenv run:**

`deactivate`

## Install requirements (inside virtualenv)

`pip install -r requirements.txt`

## Config server

Copy **config.py.example** to **config.py** and fill with the proper config information

## Run server (at server folder)

`env FLASK_APP=issues_monitoring/server.py flask run`
