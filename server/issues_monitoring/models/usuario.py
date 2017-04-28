import bcrypt
from datetime import datetime
from . import db

class UsuarioLab:
    def __init__(self, user_id, nome, email, data_aprovacao = None,
                 laboratorio = None, lab_id = None):
        self.user_id = user_id
        self.nome = nome
        self.lab_id = lab_id
        self.laboratorio = laboratorio
        self.email = email
        self.data_aprovacao = data_aprovacao

    def registrar_presenca(eventos):
        # eventos = lista de objetos da class Evento
        pass

    def cadastrar(self):
        values = (self.lab_id,
                  self.user_id,
                  self.nome,
                  self.email,
                  self.data_aprovacao)
        if not db.fetchone("""
            SELECT user_id
            FROM Presenca
            WHERE user_id = ?;""", (self.user_id,)) == self.user_id:
            db.execute("""
                INSERT INTO User_Sys
                (user_id, nome, email, data_aprov)
                VALUES (?, ?, ?, ?);""", values)
        db.execute("""
            INSERT INTO Presenca
            (user_id, lab_id, presente)
            VALUES (?, ?, ?)""", (self.user_id, self.lab_id, False))

    def remover(id_lab, user_id):
        db.execute("""
            DELETE p.*
            FROM Presenca
            WHERE id_lab = ?,
                  user_id = ?;""", (id_lab, user_id))
        count = db.fetchone("""
            SELECT COUNT(p.*
            FROM Presenca
            WHERE user_id = ?;""", (user_id,))
        if count > 0:
            db.execute("""
                DELETE u.*
                FROM User_Lab
                WHERE user_id = ?;""", (user_id,))

class UsuarioSistema:
    admin = False

    def __init__(self, login, senha, email, nome, hash = None,
                 id = None):
        self.id = id
        self.login = login
        self.senha = hash or UsuarioSistema.__hash_senha(senha)
        self.email = email
        self.nome = nome

    def cadastrar(self):
        values = (self.login,
                  self.senha,
                  self.email,
                  self.nome,
                  self.admin)
        db.execute("""
            INSERT INTO User_Sys
            (login, senha, email, nome, admin)
            VALUES (?, ?, ?, ?, ?);""", values)

    def autenticar(login, senha):
        (_id, _hash, _admin) = db.fetchone("""
            SELECT user_id, senha, admin
            FROM User_Sys
            WHERE login = ?;""", (login,)) 

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
    admin = True

    def autorizar_usuario_lab(user_id):
        data_aprovacao = int(datetime.now().timestamp())
        db.execute("""
            UPDATE User_Lab
            SET data_aprov = ?
            WHERE user_id = ?;""", (data_aprovacao, user_id))
