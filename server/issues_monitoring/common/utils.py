from datetime import datetime
from flask import session

def autenticado():
    tem_user_id = session.get('id') is not None

    expira = session.get('expiration') or 0
    nao_expirado = expira > datetime.now().timestamp()
    return nao_expirado and tem_user_id
