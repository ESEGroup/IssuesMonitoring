from flask import Flask
app = Flask(__name__)

from threading import Thread
from os import getenv
from time import sleep
try:
    from server import Config, DB
except:
    from config import Config
    from db import DB
from .controllers import reset_presencas_meia_noite, checar_condicoes_no_intervalo

class NoTokenParser(KeyboardInterrupt):
    pass

class NoEmailPassword(KeyboardInterrupt):
    pass

class NoSecretKey(KeyboardInterrupt):
    pass

if Config.token_parser == "":
    print("Please change the 'token_parser' at `config.py` (remember to update at the parser client too)")
    raise NoTokenParser
elif Config.email_password == "":
    print("Please change the 'email_password' at `config.py`")
    raise NoEmailPassword
elif not Config.debug and getenv('SECRET_KEY') is None:
    print("Please set the 'SECRET_KEY' environment "
          "variable while in production")
    print("The secret key signs the cookies allowing user "
          "authentication, leaving it empty means anyone can get "
          "authenticated as a user or admin")
    print('    export SECRET_KEY="[secret_key]";')
    raise NoSecretKey

from .common.utils import random_string
if Config.debug:
    app.config['SECRET_KEY'] = 'cmsodna oskawa j0iwjdeoj20n'
else:
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')

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
