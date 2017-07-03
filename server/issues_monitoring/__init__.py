from flask import Flask
app = Flask(__name__)

try:
    from server import Config, DB
    from ..parser.run import work as run_parser
except:
    from config import Config
    from db import DB
    from parser.run import work as run_parser

from threading import Thread
from os import getenv
from time import sleep
from .controllers import reset_presencas_meia_noite, checar_condicoes_ambiente

class NoEmailPassword(KeyboardInterrupt):
    pass

class NoSecretKey(KeyboardInterrupt):
    pass

if Config.email_password == "":
    raise NoEmailPassword("Please change the 'email_password' at `config.py`")
elif not Config.debug and getenv('SECRET_KEY') is None:
    raise NoSecretKey(
            "\n\nPlease set the 'SECRET_KEY' environment "
            "variable while in production\n"
            "The secret key signs the cookies allowing user "
            "authentication, leaving it empty means anyone can get "
            "authenticated as a user or admin\n"
            "Run this command before running the script again, "
            "filling with the a proper randomly generated key:\n"
            "    export SECRET_KEY=\"[secret_key]\";\n\n")

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

def run_threads():
    # Reset presenças as 00
    thread = Thread(target=reset_presencas_meia_noite)
    thread.daemon = True
    thread.start()

    # Thread do parser
    thread_parser = Thread(target=run_parser)
    thread_parser.daemon = True
    thread_parser.start()

    # Testa por anomalias em cada laboratório
    lab_ids = controllers.obter_laboratorios_id() 
    threads_condicoes = []
    for i in range (len(lab_ids)):
        threads_condicoes.append(
            Thread(target=checar_condicoes_ambiente,
                   args=(lab_ids[i],)))
        threads_condicoes[i].daemon = True
        threads_condicoes[i].start()

if Config.debug:
    @app.before_first_request
    def run():
        run_threads()
else:
    run_threads()
