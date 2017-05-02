from datetime import datetime
from ..models import UsuarioSistema, UsuarioLab, AdministradorSistema

def autenticar(usuario, senha):
    return UsuarioSistema.autenticar(usuario, senha)

def obter_usuarios_sistema():
    return UsuarioSistema.obter_informacoes()

def editar_status_administrador(user_id, admin):
    AdministradorSistema.editar_status_administrador(user_id, admin)

def editar_autorizacao_usuario(user_id, autorizar):
    AdministradorSistema.editar_autorizacao_usuario(user_id, autorizar)

def cadastro_usuario_sistema(login, senha, email, nome):
    if not UsuarioSistema.existe(login, email):
        usuario = UsuarioSistema(login, senha, email, nome)
        usuario.cadastrar()
        return True
    else:
        return False

def adicionar_usuario_lab(lab_id, user_id):
    UsuarioLab.adicionar_ao_laboratorio(lab_id, user_id)

def autorizar_usuario_lab(lab_id, user_id):
    AdministradorSistema.autorizar_usuario_lab(lab_id, user_id)

def obter_usuarios_laboratorio():
    return UsuarioLab.obter_todos()

def cadastro_usuario_lab(lab_id, user_id, nome, email, aprovar=False):
    if not UsuarioLab.existe(user_id):
        data_aprovacao = None
        if aprovar:
            data_aprovacao = int(datetime.now().timestamp())

        usuario = UsuarioLab(user_id,
                             nome,
                             email,
                             data_aprovacao,
                             lab_id=lab_id)
        usuario.cadastrar()
        return True
    else:
        return False

def remover_usuario_lab(id_lab, user_id):
    UsuarioLab.remover(id_lab, user_id)
