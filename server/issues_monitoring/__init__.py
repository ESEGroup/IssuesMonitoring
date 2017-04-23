from flask import Flask

app = Flask(__name__)

from ..config import Config
from os       import getenv
app.config['SECRET_KEY'] = getenv('SECRET_KEY') or Config.secret_key
