import bcrypt
import sqlite3
from ...db import DB

class UsuarioLab:
    def __init__(self, lab_id, user_id, nome, email, data_aprovacao = None,
                 laboratorio = None):
        self.lab_id = lab_id
        self.user_id = user_id
        self.nome = nome
        self.laboratorio = laboratorio
        self.email = email
        self.data_aprovacao = data_aprovacao

    def registrar_presenca(eventos):
        # eventos = lista de objetos da class Evento
        pass

    def cadastrar(self):
        pass

    def remover(id_lab, user_id):
        pass

class UsuarioSistema:
    def __init__(self, login, senha, email, nome, hash = None,
                 id = None):
        self.id = id
        self.login = login
        self.senha = hash or UsuarioSistema.__hash_senha(senha)
        self.email = email
        self.nome = nome

    def cadastrar(self):
        pass

    def autenticar(login, senha):
        # Obter hash do usuário do banco de dados, se usuário não
        # existir ou autenticação falhar, retornar None, se autenticar,
        # retornar 'id' e flag 'admin', obtidas do banco de dados
        _id = None
        _hash = None
        admin = False
        if UsuarioSistema.__hash_senha(senha, _hash) == _hash:
            return _id, admin
        return None, False


    def __hash_senha(senha, _hash = None):
        if isinstance(senha, str):
            senha = bytes(senha, 'utf-8')

        if _hash is None:
            _hash = bcrypt.gensalt()
        elif isinstance(_hash, str):
            _hash = bytes(_hash, 'utf-8')

        return bcrypt.hashpw(senha, _hash).decode('utf-8')

def AdministradorSistema(UsuarioSistema):
    def autorizar_usuario_lab(user_id):
        pass
