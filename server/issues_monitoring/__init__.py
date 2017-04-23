from flask import Flask

app = Flask(__name__)

from ..config import Config
from .views import Views
