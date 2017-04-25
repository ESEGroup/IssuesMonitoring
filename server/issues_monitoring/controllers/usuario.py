from ..models import UsuarioSistema

def autenticado(session):
    tem_user_id = session.get('user_id') is not None

    expira = session.get('expiration') or 0
    nao_expirado = expira > datetime.now().timestamp()
    return nao_expirado and tem_user_id

def autenticar_usuario(usuario, senha):
    return UsuarioSistema.autenticar(usuario, senha)
