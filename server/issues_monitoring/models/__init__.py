from ...db import DB
from .. import Config
db = DB(Config.db_path)

from .laboratorio import *
from .usuario import *

