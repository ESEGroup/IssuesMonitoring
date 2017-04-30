from . import db
from .usuario_lab import UsuarioLab
from .equipamento import Equipamento
from .zona_conforto import ZonaConforto

class Laboratorio:
    def __init__(self, nome, endereco, intervalo_parser,
                 intervalo_arduino, zona_conforto_lab = None,
                 id = None, equipamentos = [], membros = []):
        self.nome = nome
        self.endereco = endereco
        self.intervalo_parser = intervalo_parser
        self.intervalo_arduino = intervalo_arduino
        self.zona_conforto_lab = zona_conforto_lab
        self.id = id
        self.equipamentos = equipamentos
        self.membros = membros

    def registrar_medidas(_id, temperatura, luminosidade, umidade):
        data_registro = int(datetime.now().timestamp())

    def obter_medidas(_id):
        pass

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

    def obter_todos():
        data = db.fetchall("SELECT nome, lab_id FROM Lab")
        return [Laboratorio(d[0], None, None, None, None, d[1]) for d in data]

    def obter_informacoes():
        data = db.fetchall("""
            SELECT l.lab_id, l.nome, l.endereco, l.intervalo_parser,
            l.intervalo_arduino, zc.temp_min, zc.temp_max,
            zc.umid_min, zc.umid_max, zc.lum_min, zc.lum_max, l.lab_id,
            e.temp_min, e.temp_max, e.end_mac, e.equip_id, u.user_id,
            u.nome, u.email, u.data_aprov
            FROM Lab as l
            INNER JOIN Zona_de_Conforto_Lab as zc
              ON l.zona_conforto_id = zc.zona_conforto_id
            LEFT JOIN Presenca as p
              ON l.lab_id = p.lab_id
            LEFT JOIN User_Lab as u
              ON p.user_id = u.user_id
            LEFT JOIN Equip as e
              ON l.lab_id = e.lab_id;""")

        _dict = {}
        equipamentos_id = {}
        usuarios_id = {}
        for d in data:
            equipamentos_id.setdefault(d[0], {None})
            usuarios_id.setdefault(d[0], {None})

            usuario_lab = UsuarioLab(*d[-4:])
            equipamento = Equipamento(*d[-9:-4])
            zona_conforto = ZonaConforto(*d[5:-9])
            lab_info = list(d[1:5]) + [zona_conforto]
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
        now = int(datetime.now().timestamp())
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
        return db.fetchone("""
            SELECT intervalo_parser
            FROM Lab;""")[0]

    def obter_intervalo_arduino(lab_id):
        return db.fetchone("""
            SELECT intervalo_arduino
            FROM Lab
            WHERE lab_id = ?;""", (lab_id,))
