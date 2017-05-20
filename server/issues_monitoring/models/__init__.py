from .. import Config, DB
db = DB(Config.db_path)

from .laboratorio import Laboratorio
from .zona_conforto import ZonaConforto
from .evento import Evento
from .equipamento import Equipamento

from .usuario import Usuario
from .usuario_lab import UsuarioLab
from .usuario_sistema import UsuarioSistema
from .administrador_sistema import AdministradorSistema

from .arduino import Arduino
from .medida import Medida_Equip, Medida_Lab
