from threading import Thread
from flask import Flask
from os import getenv
from time import sleep
from ..config import Config
from .controllers import reset_presencas_meia_noite

app = Flask(__name__)

app.config['SECRET_KEY'] = getenv('SECRET_KEY') or "7612367hfyy8923u4dryr12ybri2bi8yniis1b"

# Reset presenças as 00
thread = Thread(target=reset_presencas_meia_noite)
thread.daemon = True
thread.start()
