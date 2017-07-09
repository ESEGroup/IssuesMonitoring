import bcrypt
from ..common.erros import NaoAutorizado, InformacoesIncorretas
from .usuario import Usuario
from . import db

class UsuarioSistema(Usuario):
    admin = False

    def __init__(self, login, senha, email, nome, id = None,
                 data_aprovacao = None, hash = False):
        super().__init__(nome, email, data_aprovacao)
        self.id = id
        self.login = login
        if hash:
            self.senha = senha
        else:
            self.senha = UsuarioSistema.__hash_senha(senha)
        self.email = email
        self.nome = nome

    def obter(user_id):
        data = db.fetchone("""
            SELECT admin, login, senha, email, nome, user_id, data_aprov
            FROM User_Sys
            WHERE user_id = ?;""",
            (user_id,))
        usuario = UsuarioSistema(*data[1:], hash=True)
        usuario.admin = bool(int(data[0]))
        return usuario

    def obter_informacoes():
        data = db.fetchall("""
            SELECT admin, login, senha, email, nome, user_id, data_aprov
            FROM User_Sys;""")
        usuarios = []
        for d in data:
            usuarios += [UsuarioSistema(*d[1:], hash=True)]
            usuarios[-1].admin = bool(int(d[0]))
        return usuarios

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

    def alterar_senha(login, senha):
        db.execute("""
            UPDATE User_Sys
            SET senha = ?
            WHERE login = ?""",
            (UsuarioSistema.__hash_senha(senha), login))
        return True

    def autenticar(login, senha):
        args = db.fetchone("""
            SELECT user_id, senha, admin, data_aprov
            FROM User_Sys
            WHERE login = ?;""", (login,))
        if args is None:
            raise InformacoesIncorretas

        (_id, _hash, _admin, data_aprov) = args
        if data_aprov is None:
            raise NaoAutorizado
        if UsuarioSistema.__hash_senha(senha, _hash) == _hash:
            return _id, _admin
        else:
            raise InformacoesIncorretas

    def existe(login, email):
        return db.fetchone("""
            SELECT user_id
            FROM User_Sys
            WHERE login = ?
                  OR email = ?;""",
            (login, email)) is not None

    def editar(self):
        db.execute("""UPDATE User_Sys
                   SET nome = ?,
                       email = ?,
                       login = ?
                   WHERE user_id = ?;""",
                   (self.nome,
                    self.email,
                    self.login,
                    self.id))

    def remover(id):
        db.execute("""DELETE FROM User_Sys
                   WHERE user_id = ?;""",
                   (id,))

    def __hash_senha(senha, _hash = None):
        if isinstance(senha, str):
            senha = bytes(senha, 'utf-8')

        if _hash is None:
            _hash = bcrypt.gensalt()
        elif isinstance(_hash, str):
            _hash = bytes(_hash, 'utf-8')

        return bcrypt.hashpw(senha, _hash).decode('utf-8')
