from datetime import datetime
from ..models import UsuarioSistema, UsuarioLab

def autenticar(usuario, senha):
    return UsuarioSistema.autenticar(usuario, senha)

def cadastrar_usuario_lab(lab_id, user_id, nome, email, aprovar=False):
    if aprovar:
        data_aprovacao = int(datetime.now().timestamp())
    else:
        data_aprovacao = None
    usuario = UsuarioLab(lab_id, user_id, nome, email, data_aprovacao)
    return usuario.cadastrar()

def remover_usuario_lab(id_lab, user_id):
    return UsuarioLab.remover(id_lab, user_id)

def cadastrar_usuario_sistema(login, senha, email, nome):
    usuario = UsuarioSistema(login, senha, email, nome)
    return usuario.cadastrar()
