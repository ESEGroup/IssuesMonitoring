from ...db import DB
from .. import Config
db = DB(Config.db_path)

from .laboratorio import *
from .zona_conforto import *
from .evento import *
from .equipamento import *

from .usuario_lab import *
from .usuario_sistema import *
from .administrador_sistema import *
