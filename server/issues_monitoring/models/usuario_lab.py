from datetime import datetime
from ..common.utils import hoje
from ..common.erros import UsuarioLabJaCadastrado
from .evento import Evento
from .usuario import Usuario
from . import db

class UsuarioLab(Usuario):
    def __init__(self, user_id, nome, email, data_aprovacao = None,
                 laboratorio = None, lab_id = None, data_entrada = None, data_evento = None, evento = None, id = None):
        super().__init__(nome, email, data_aprovacao)
        self.user_id = user_id
        self.nome = nome
        self.email = email
        self.data_aprovacao = data_aprovacao
        self.lab_id = lab_id
        self.laboratorio = laboratorio
        self.data_entrada = data_entrada
        self.data_evento = data_evento
        self.evento = evento
        self.id = id

    def obter(user_id):
        data = db.fetchone("""SELECT id, user_id, nome, email, data_aprov
                           FROM User_Lab
                           WHERE user_id = ?;""",
                           (user_id,))
        if data is None:
            return data

        return UsuarioLab(*data[1:], id=data[0])

    def obter_todos():
        data = db.fetchall("SELECT id, user_id, nome, email, data_aprov FROM User_Lab")
        return [UsuarioLab(*d[1:], id=d[0]) for d in data]

    def obter_do_laboratorio(id):
        data = db.fetchall("""SELECT u.id, u.user_id, u.nome, u.email, u.data_aprov
                            FROM User_Lab u
                            INNER JOIN Presenca p
                              ON p.user_id = u.user_id
                            WHERE p.lab_id = ?;""", (id,))
        return [UsuarioLab(*d[1:], id=d[0]) for d in data]

    def registrar_presenca(eventos):
        usuarios_presenca = []
        tupla_eventos = []
        for e in eventos:
            usuarios_presenca += [(e.evento == "IN", e.user_id, e.lab_id)]
            tupla_eventos += [(e.epoch,
                               e.user_id,
                               e.lab_id,
                               e.evento)]

        db.executemany("""
            UPDATE Presenca
            SET presente = ?
            WHERE user_id = ?
                  AND lab_id = ?;""",
            usuarios_presenca)
        db.executemany("""
            INSERT INTO Log_Presenca
            (data, user_id, lab_id, evento)
            VALUES (?, ?, ?, ?);""",
            tupla_eventos)

    def existe(user_id):
        return db.fetchone("""
            SELECT user_id
            FROM User_lab
            WHERE user_id = ?;""", (user_id,)) is not None

    def presentes(lab_id):
        data = db.fetchall("""SELECT u.user_id, u.nome, u.email,
                                     u.data_aprov, log.data
                            FROM User_Lab u
                            INNER JOIN Presenca p
                                ON p.user_id = u.user_id
                            INNER JOIN Log_Presenca log
                                ON log.user_id = u.user_id
                                   AND log.lab_id = p.lab_id
                            WHERE log.evento = "IN"
                                  AND p.presente = ?
                                  AND p.lab_id = ?
                            ORDER BY log.data DESC;""",
                            (True,
                             lab_id))
        usuarios = []
        usuarios_set = set()
        for d in data:
            if d[0] not in usuarios_set:
                usuarios_set.add(d[0])
                usuarios += [UsuarioLab(*d[:-1], data_entrada=d[-1])]
        return usuarios

    def cadastrar(self):
        values = (self.user_id,
                  self.nome,
                  self.email,
                  self.data_aprovacao)

        data = UsuarioLab.obter(self.user_id)

        if data is not None:
            raise UsuarioLabJaCadastrado

        db.execute("""
            INSERT INTO User_Lab
            (user_id, nome, email, data_aprov)
            VALUES (?, ?, ?, ?);""", values)

        UsuarioLab.adicionar_ao_laboratorio(self.lab_id,
                                            self.user_id)

    def editar(self, old_user_id=None):
        db.execute("""
            UPDATE User_Lab
            SET nome = ?,
                email = ?,
                user_id = ?
            WHERE id = ?;""",
            (self.nome,
             self.email,
             self.user_id,
             self.id))
        if old_user_id is not None:
            db.execute("""
                UPDATE Presenca
                SET user_id = ?
                    WHERE user_id = ?;""",
                    (self.user_id,
                    old_user_id))

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

    def eventos(lab_id, dia):
        prox_dia = dia + 60 * 60 * 24 + 1
        dia -= 1

        data = db.fetchall("""
            SELECT l.data, l.evento, l.user_id, l.lab_id, u.nome
            FROM Log_Presenca l
            INNER JOIN User_Lab u
              ON u.user_id = l.user_id
            WHERE l.lab_id = ?
                  AND l.data > ?
                  AND l.data < ?
            ORDER BY l.data DESC;""",
            (lab_id, dia, prox_dia)) or []
        return [Evento(*d) for d in data]

    def data_proximo_evento(lab_id, dia):
        dia_dt = datetime.fromtimestamp(dia)
        dia = int(datetime(day=dia_dt.day,
                           month=dia_dt.month,
                           year=dia_dt.year,
                           hour=23,
                           minute=59,
                           second=59).timestamp())
        data = db.fetchone("""SELECT data
                           FROM Log_Presenca
                           WHERE lab_id = ?
                                 AND data > ?
                           ORDER BY data ASC;""",
                           (lab_id,
                            dia))
        if data is not None:
            return data[0]
        return dia_dt.timestamp()

    def data_evento_anterior(lab_id, dia):
        data = db.fetchone("""SELECT data
                           FROM Log_Presenca
                           WHERE lab_id = ?
                                 AND data < ?
                           ORDER BY data DESC;""",
                           (lab_id,
                            dia))
        if data is not None:
            return data[0]
        return dia

    def obter_dado_presenca(hoje, amanha, lab_id):
        data = db.fetchall("""
                SELECT u.user_id, u.nome, u.email, l.data, l.evento
                FROM Log_Presenca l
                INNER JOIN User_Lab u
                  ON l.user_id = u.user_id
                WHERE l.lab_id = ?
                      AND l.data >= ?
                      AND l.data <= ?
                ORDER BY data DESC""",
                (lab_id, hoje, amanha))
        log_presenca = []
        for d in data:
            log_presenca += [UsuarioLab(*d[:-2], data_evento=d[-2], evento=d[-1])]
        return log_presenca

    def user_ids_registradas(user_ids):
        values = ', '.join("?" for i in user_ids)
        data = db.fetchall("""
            SELECT user_id
            FROM User_Lab
            WHERE user_id in ({})""".format(values),
            user_ids)
        return [d[0] for d in data]

    def adicionar_ao_laboratorio(lab_id, user_id):
        if db.fetchone("""
            SELECT user_id
            FROM Presenca
            WHERE user_id = ?
                AND lab_id = ?;""",
                (user_id, lab_id)) is not None:
            return

        db.execute("""
            INSERT INTO Presenca
            (lab_id, user_id, presente)
            VALUES (?, ?, ?);""",
            (lab_id,
            user_id,
            False))
