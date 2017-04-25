from ..models import UsuarioSistema, UsuarioLab

def autenticar(usuario, senha):
    return UsuarioSistema.autenticar(usuario, senha)

def cadastrar_usuario_lab(user_id, nome, email):
    usuario = UsuarioLab(user_id, nome, email)
    return usuario.cadastrar()
