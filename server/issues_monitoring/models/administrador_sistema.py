from datetime import datetime
from .usuario_sistema import UsuarioSistema
from . import db

class AdministradorSistema(UsuarioSistema):
    admin = True

    def autorizar_usuario_lab(lab_id, user_id):
        data_aprovacao = int(datetime.now().timestamp())
        db.execute("""
            UPDATE User_Lab
            SET data_aprov = ?
            WHERE user_id = ?;""", (data_aprovacao,
                                    user_id))
    def editar_autorizacao_usuario(user_id, aprovar):
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

