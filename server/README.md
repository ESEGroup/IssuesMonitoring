# How to deploy the server

## Clone the repository

SSH:

`git clone git@github.com:ESEGroup/IssuesMonitoring.git`

HTTPS:

`git clone https://github.com/ESEGroup/IssuesMonitoring.git`

## Install python 3 and virtualenv

Ubuntu:

`sudo apt-get install python3 python3-pip virtualenv`

## Run build script

`python3 build.py`

## Configure server

Necessary changes:

- 'token_parser' (also change at parser client)

In production:

- 'debug' to False

- 'issues_monitoring' port from 8080 to 80 


## Join the virtualenv

`source .env/bin/activate`

**To leave the virtualenv run:**

`deactivate`

## Run server (inside virtualenv)

GNU/Linux:

`bash run`

General:

`env FLASK_APP=issues_monitoring/server.py flask run`
