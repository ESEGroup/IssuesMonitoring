from datetime import datetime
from .usuario_sistema import UsuarioSistema
from . import db

class AdministradorSistema(UsuarioSistema):
    admin = True

    def obter_administradores():
        data = db.fetchall("""
            SELECT login, senha, email, nome, user_id, data_aprov
            FROM User_Sys
            WHERE admin = 1;""")
        admins = []
        for d in data:
            admins += [AdministradorSistema(*d, hash=True)]
        return admins

    def autorizar_usuario_lab(user_id, autorizar):
        if autorizar:
            data_aprovacao = int(datetime.now().timestamp())
        else:
            data_aprovacao = None
        db.execute("""
            UPDATE User_Lab
            SET data_aprov = ?
            WHERE user_id = ?;""", (data_aprovacao,
                                    user_id))

    def aprovar_usuario(user_id, aprovar):
        if aprovar:
            data_aprovacao = int(datetime.now().timestamp())
        else:
            data_aprovacao = None
        db.execute("""
            UPDATE User_Sys
            SET data_aprov = ?
            WHERE user_id = ?;""", (data_aprovacao,
                                    user_id))

    def editar_status_administrador(user_id, admin):
        db.execute("""
            UPDATE User_Sys
            SET admin = ?
            WHERE user_id = ?;""", (admin, user_id))
