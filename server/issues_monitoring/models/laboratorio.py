from . import db
from .usuario_lab import UsuarioLab
from .computador import Computador
from .zona_conforto import ZonaConforto
from .medida import Medida_Lab, Medida_Equip
from datetime import datetime

class Laboratorio:
    def __init__(self, nome, endereco, intervalo_parser,
                 intervalo_arduino, zona_conforto_lab = None,
                 id = None, equipamentos = [], membros = []):
        self.nome              = nome
        self.endereco          = endereco
        self.intervalo_parser  = intervalo_parser
        self.intervalo_arduino = intervalo_arduino
        self.zona_conforto_lab = zona_conforto_lab
        self.id                = id
        self.equipamentos      = equipamentos
        self.membros           = membros

    def obter_ultima_medida(lab_id, data_inicio, data_final):
        data = db.fetchone("""
            SELECT data, temp, umid, lum
            FROM Log_Lab
            WHERE lab_id = ?
                  AND data > ?
                  AND data <= ?
            ORDER BY data DESC; """, (lab_id,
                                      data_inicio,
                                      data_final))
        if data is not None:
            return data
        return [None, None, None, None]

    def registrar_medidas(medida):
        epoch = int(datetime.today().timestamp())
        #insert lab info
        db.execute('''
            INSERT INTO Log_Lab
            (data, lab_id, temp, umid, lum)
            VALUES (?, ?, ?, ?, ?);''', (epoch, medida.lab_id, medida.term_sens, medida.hum, medida.lum))

        for m in medida.medidas_equips:
            # foreach equip, insert its info
            db.execute('''
                INSERT INTO Log_Equip
                (data, equip_id, temp)
                VALUES (?, ?, ?);''', (epoch, m.equip_id, m.temp))

    def cadastrar(self):
        args = (self.zona_conforto_lab.id,
                self.nome,
                self.endereco,
                self.intervalo_parser,
                self.intervalo_arduino)
        self.id = db.execute("""
            INSERT INTO Lab
            (zona_conforto_id, nome, endereco, intervalo_parser,
             intervalo_arduino)
            VALUES (?, ?, ?, ?, ?);""", args,
            return_id=True)

    def obter(id):
        data = db.fetchone("""SELECT nome, endereco, intervalo_parser,
                                     intervalo_arduino, lab_id
                              FROM LAB
                              WHERE lab_id = ?;""", (id,))
        if data is not None:
            return Laboratorio(*data[:-1],
                               id=data[-1])

    def obter_todos():
        data = db.fetchall("SELECT nome, lab_id FROM Lab")
        return [Laboratorio(d[0], None, None, None, None, d[1]) for d in data]

    def obter_todos_ids():
        data = db.fetchall("SELECT lab_id FROM Lab;")
        return [d[0] for d in data]

    def obter_informacoes():
        data = db.fetchall("""
            SELECT l.lab_id, l.nome, l.endereco, l.intervalo_parser,
            l.intervalo_arduino, zc.temp_min, zc.temp_max,
            zc.umid_min, zc.umid_max, l.lab_id,
            e.nome, e.descricao, e.temp_min, e.temp_max, e.end_mac, e.parent_id, e.equip_id,
            u.user_id, u.nome, u.email, u.data_aprov
            FROM Lab as l
            INNER JOIN Zona_de_Conforto_Lab as zc
              ON l.zona_conforto_id = zc.zona_conforto_id
            LEFT JOIN Presenca as p
              ON l.lab_id = p.lab_id
            LEFT JOIN User_Lab as u
              ON p.user_id = u.user_id
            LEFT JOIN Equip as e
              ON l.lab_id = e.lab_id;""")

        _dict           = {}
        equipamentos_id = {}
        usuarios_id     = {}
        for d in data:
            equipamentos_id.setdefault(d[0], {None})
            usuarios_id.setdefault(d[0], {None})

            usuario_lab   = UsuarioLab(*d[-4:])
            equipamento   = Computador(*d[9:-4])
            zona_conforto = ZonaConforto(*d[5:10])
            lab_info      = list(d[1:5]) + [zona_conforto]

            _dict.setdefault(d[0], Laboratorio(*lab_info,
                                               membros=[],
                                               equipamentos=[],
                                               id=d[0]))

            if equipamento.id not in equipamentos_id[d[0]]:
                _dict[d[0]].equipamentos += [equipamento]

            if usuario_lab.user_id not in usuarios_id[d[0]]:
                _dict[d[0]].membros += [usuario_lab]

            usuarios_id[d[0]].add(usuario_lab.user_id)
            equipamentos_id[d[0]].add(equipamento.id)
        return sorted(_dict.values(), key=lambda d: d.id)

    def editar(self):
        db.execute("""
            UPDATE Lab
            SET nome = ?,
                endereco = ?,
                intervalo_parser = ?,
                intervalo_arduino = ?
            WHERE lab_id = ?;""",
            (self.nome,
             self.endereco,
             self.intervalo_parser,
             self.intervalo_arduino,
             self.id))

    def reset_lista_presenca():
        data = db.fetchall("""
            SELECT p.user_id, u.email, p.lab_id
            FROM Presenca p
            INNER JOIN User_Lab u
              ON p.user_id = u.user_id
            WHERE presente = 1;""")

        events = []
        emails = []
        now = int(datetime.today().timestamp())
        for d in data:
            events += [(now, d[0], d[2], "OUT")]
            emails += [d[1]]

        db.execute("""
            UPDATE Presenca
            SET presente = 0;""")

        db.executemany("""
            INSERT INTO Log_Presenca
            (data, user_id, lab_id, evento)
            VALUES (?, ?, ?, ?);""",
            events)
        return emails

    def obter_intervalo_parser():
        data = db.fetchone("""
            SELECT intervalo_parser
            FROM Lab;""")
        if data is not None:
            return data[0]
        return -1

    def obter_intervalo_arduino(lab_id):
        data = db.fetchone("""
            SELECT intervalo_arduino
            FROM Lab
            WHERE lab_id = ?;""", (lab_id,))
        if data is not None:
            return data[0]
        return "-10"

    def ultima_atualizacao_parser():
        data = db.fetchone("""
            SELECT data
            FROM Log_Parser
            ORDER BY data DESC;""")
        if data is not None:
            return data[0]
        return "-10"

    def ultima_atualizacao_arduino(_id):
        data = db.fetchone("""
            SELECT data
            FROM Log_Lab
            WHERE lab_id = ?
            ORDER BY data DESC;""", (_id,))
        if data is not None:
            return data[0]

    def registrar_log_parser():
        epoch = int(datetime.today().timestamp())
        db.execute('''
            INSERT INTO Log_Parser
            (data)
            VALUES (?);''', (epoch,))
        return True

    def remover(id):
        db.execute("""
            DELETE FROM Zona_de_Conforto_Lab
            WHERE zona_conforto_id in (
                SELECT zona_conforto_id FROM Lab
                WHERE lab_id = ?);""", (id,))
        db.execute("""
            DELETE FROM Lab
            WHERE lab_id = ?;""", (id,))

    def obter_todos_ids_equipamentos(id):
        data = db.fetchall("SELECT equip_id FROM Equip WHERE lab_id=?",(id,))

        equipamentos = []
        for d in data:
            if d[0] not in equipamentos:
                equipamentos.append(d[0])
        return equipamentos

    def obter_nome_equipamentos(id):
        data = db.fetchall("SELECT equip_id, nome FROM Equip WHERE lab_id=?",(id,))

        equipamentos = {}
        for d in data:
            equipamentos[d[0]] = d[1]
        return equipamentos

    def nome(lab_id):
        data = db.fetchone("""SELECT nome FROM Lab WHERE lab_id = ?;""", (lab_id,))
        if data is not None:
            return data[0]

    def presentes(lab_id):
        data = db.fetchall("""
            SELECT u.email
            FROM Presenca p
            INNER JOIN User_Lab u
              ON p.user_id = u.user_id
            WHERE presente = 1 AND lab_id = ?; """, (lab_id,))

        emails = []
        if len(data) != 0:
            for d in data:
                emails += [d[0]]
        return emails

    def email_ultimo_a_sair(lab_id):
        data = db.fetchone("""SELECT u.email
                              FROM Log_Presenca l, User_Lab u
                              WHERE l.lab_id=?
                                    AND l.evento='OUT'
                                    AND l.user_id = u.user_id
                              ORDER BY l.data DESC;""", (lab_id,))

        if data is not None:
            return [data[0]]
        return []

    def obter_temperatura_entre_tempos_lab(tempo_inicio, tempo_final, lab_id):
        data = db.fetchall("""
            SELECT data, temp
            FROM Log_Lab
            WHERE lab_id = ?
                  AND data >= ?
                  AND data < ?
            ORDER BY data ASC;""", (lab_id, tempo_inicio, tempo_final))

        if data is not None:
            return data

        return []

    def obter_umidade_entre_tempos_lab(tempo_inicio, tempo_final, lab_id):
        data = db.fetchall("""
            SELECT data, umid
            FROM Log_Lab
            WHERE lab_id = ?
                  AND data >= ?
                  AND data < ?
            ORDER BY data ASC;""", (lab_id, tempo_inicio, tempo_final))

        if data is not None:
            return data

        return []

    def obter_dados_entre_tempos_lab(tempo_inicio, tempo_final, lab_id):
        data = db.fetchall("""
            SELECT data, temp, umid
            FROM Log_Lab
            WHERE lab_id = ?
                  AND data >= ?
                  AND data < ?
            ORDER BY data ASC;""", (lab_id, tempo_inicio, tempo_final))

        if data is not None:
            return data
        return []
