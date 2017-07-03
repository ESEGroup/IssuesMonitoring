# Build environment

## Clone the repository

SSH:

`git clone git@github.com:ESEGroup/IssuesMonitoring.git`

HTTPS:

`git clone https://github.com/ESEGroup/IssuesMonitoring.git`

## Install python 3, virtualenv and [wkhtmltopdf](https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf), xvfb

Ubuntu:

`sudo apt-get install python3 python3-pip wkhtmltopdf xvfb virtualenv`

## Run build script

`python3 build.py`

## Configure server

Edit **config.py**

Necessary changes (empty is not accepted):

- 'email_password'

In production:

- 'debug' to False

- 'issues_monitoring' port from 8080 to 80 

# Run server

## Join the virtualenv

`source .env/bin/activate`

**To leave the virtualenv run:**

`deactivate`

## Run server (inside virtualenv)

GNU/Linux:

`bash run` 

or `./run` after the first execution

General:

`python3 run.py`
