from .usuario import Usuario
from . import db

class UsuarioLab(Usuario):
    def __init__(self, user_id, nome, email, data_aprovacao = None,
                 laboratorio = None, lab_id = None):
        super().__init__(nome, email, data_aprovacao)
        self.user_id = user_id
        self.nome = nome
        self.email = email
        self.data_aprovacao = data_aprovacao
        self.lab_id = lab_id
        self.laboratorio = laboratorio

    def registrar_presenca(eventos):
        usuarios_presenca = []
        tupla_eventos = []
        for e in eventos:
            usuarios_presenca += [(e.evento == "IN", e.user_id)]
            tupla_eventos += [(e.epoch, e.user_id, e.lab_id, e.evento)]

        db.executemany("""
            UPDATE Presenca
            SET presente = ?
            WHERE user_id = ?;""",
            usuarios_presenca)
        db.executemany("""
            INSERT INTO Log_Presenca
            (data, user_id, lab_id, evento)
            VALUES (?, ?, ?, ?);""",
            tupla_eventos)

    def cadastrar(self):
        values = (self.user_id,
                  self.nome,
                  self.email,
                  self.data_aprovacao)
        user_id = db.fetchone("""
            SELECT user_id
            FROM User_lab
            WHERE user_id = ?;""", (self.user_id,))
        if user_id is None:
            db.execute("""
                INSERT INTO User_Lab
                (user_id, nome, email, data_aprov)
                VALUES (?, ?, ?, ?);""", values)

        db.execute("""
            INSERT INTO Presenca
            (user_id, lab_id, presente)
            VALUES (?, ?, ?)""", (self.user_id, self.lab_id, False))

    def remover(lab_id, user_id):
        db.execute("""
            DELETE FROM Presenca
            WHERE lab_id = ? AND
                  user_id = ?;""", (lab_id, user_id))
        count = db.fetchone("""
            SELECT COUNT(presenca_id)
            FROM Presenca
            WHERE user_id = ?;""", (user_id,))[0]
        if count == 0:
            db.execute("""
                DELETE FROM User_Lab
                WHERE user_id = ?;""", (user_id,))
