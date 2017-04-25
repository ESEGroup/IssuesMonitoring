from flask import Flask

app = Flask(__name__)

from os import getenv
app.config['SECRET_KEY'] = getenv('SECRET_KEY') or "7612367hfyy8923u4dryr12ybri2bi8yniis1b"

from ..config import Config
from .views   import Views
