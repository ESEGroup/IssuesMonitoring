import bcrypt
from . import db

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
        args = db.fetchone("""
            SELECT user_id, senha, admin
            FROM User_Sys
            WHERE login = ?;""", (login,)) 

        if args is not None and len(args) == 3:
            (_id, _hash, _admin) = args

            if UsuarioSistema.__hash_senha(senha, _hash) == _hash:
                return _id, _admin

        return None, False

    def __hash_senha(senha, _hash = None):
        if isinstance(senha, str):
            senha = bytes(senha, 'utf-8')

        if _hash is None:
            _hash = bcrypt.gensalt()
        elif isinstance(_hash, str):
            _hash = bytes(_hash, 'utf-8')

        return bcrypt.hashpw(senha, _hash).decode('utf-8')
