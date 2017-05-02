from threading import Thread
from flask import Flask
from os import getenv
from time import sleep
from ..config import Config
from .controllers import reset_presencas_meia_noite

if Config.token_parser == "":
    print("Please change the 'token_parser' at `config.py` (remember to update at the parser client too)")
    exit()
elif Config.email_password == "":
    print("Please change the 'email_password' at `config.py`")
    exit()

app = Flask(__name__)

from .common.utils import random_string
if Config.debug:
    app.config['SECRET_KEY'] = 'cmsodna oskawa j0iwjdeoj20n'
else:
    app.config['SECRET_KEY'] = getenv('SECRET_KEY') or random_string(32)

@app.after_request
def no_cache_dynamic(response):
    if 'text/html' in response.headers.get('Content-Type', []):
        response.headers['Cache-Control'] = ('private,'
                                             'no-cache,'
                                             'no-store,'
                                             'must-revalidate,'
                                             'max-age=0')
        response.headers['Expire'] = '-1'
        response.headers['Pragma'] = 'no-cache'
    return response

# Reset presenças as 00
thread = Thread(target=reset_presencas_meia_noite)
thread.daemon = True
thread.start()
