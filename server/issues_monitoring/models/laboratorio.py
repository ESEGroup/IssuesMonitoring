from . import db
from .usuario import UsuarioLab

class ZonaConforto:
    def __init__(self, temp_min, temp_max, umidade_min, umidade_max,
                 lumin_min, lumin_max):
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.umidade_min = umidade_min
        self.umidade_max = umidade_max
        self.lumin_min = lumin_min
        self.lumin_max = lumin_max

class Equipamento:
    def __init__(self, lab_id, temp_min, temp_max, MAC, id = None):
        self.id = id
        self.lab_id = lab_id
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.MAC = MAC

    def obter_medidas(_id):
        pass

    def registrar_medidas(_id, temperatura):
        data_registro = int(datetime.now().timestamp())

    def cadastrar(self):
        db.execute("""
            INSERT INTO Equip
            (lab_id, temp_min, temp_max, end_mac)
            VALUES (?, ?, ?, ?)""",
            (self.lab_id,
            self.temp_min,
            self.temp_max,
            self.MAC))

    def remover(_id):
        db.execute("""
            DELETE FROM Equip
            WHERE equip_id = ?;""", (_id,))

class Evento:
    def __init__(self, epoch, evento, user_id, lab_id):
        self.epoch = epoch
        self.evento = evento
        self.user_id = user_id
        self.lab_id = lab_id

class Laboratorio:
    def __init__(self, nome, endereco, intervalo_parser,
                 intervalo_arduino, zona_conforto_lab, id = None,
                 equipamentos = [], membros = []):
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
        args = (zona_conforto_id,
                nome,
                endereco,
                intervalo_parser,
                intervalo_arduino)
        db.execute("""
            INSERT INTO Lab
            (zona_conforto_id, nome, endereco, intervalo_parser,
             intervalo_arduino)
            VALUES (?, ?, ?, ?, ?);""", args)

    def listar_todos():
        data = db.fetchall("SELECT nome, lab_id FROM Lab")
        return [Laboratorio(d[0], None, None, None, None, d[1]) for d in data]

    def editar_zona_conforto(_id, zona_conforto_lab):
        db.execute("""
            UPDATE FROM Zona_de_Conforto_Lab as zc
            SET temp_min = ?,
                temp_max = ?,
                umid_min = ?,
                umid_max = ?,
                lum_min = ?,
                lum_max = ?
            INNER JOIN Lab as l
              ON l.zona_conforto_id = zc.zona_conforto_id
            WHERE l.lab_id = ?;""",
            (zona_conforto_lab.temp_min,
             zona_conforto_lab.temp_max,
             zona_conforto_lab.umid_max,
             zona_conforto_lab.umid_min,
             zona_conforto_lab.lum_max,
             zona_conforto_lab.lum_max))

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
        equipamentos_id = {None}
        usuarios_id = {None}
        for d in data:
            usuario_lab = UsuarioLab(*d[-4:])
            equipamento = Equipamento(*d[-9:-4])
            zona_conforto = ZonaConforto(*d[5:-9])
            _dict.setdefault(d[0], Laboratorio(*d[1:5],
                                               zona_conforto,
                                               membros=[],
                                               equipamentos=[],
                                               id=d[0]))
            if equipamento.id not in equipamentos_id:
                _dict[d[0]].equipamentos += [equipamento]

            if usuario_lab.user_id not in usuarios_id:
                _dict[d[0]].membros += [usuario_lab]

            usuarios_id.add(usuario_lab.user_id)
            equipamentos_id.add(equipamento.id)

        return sorted(_dict.values(), key=lambda d: d.id)

    def editar_laboratorio(nome, endereco, intervalo_parser, intervalo_arduino):
        db.execute("""
            UPDATE Lab
            SET nome = ?,
                endereco = ?,
                intervalo_parser = ?,
                intervalo_arduino = ?;""",
            (nome,
            endereco,
            intervalo_parser,
            intervalo_arduino))

    def reset_lista_presenca():
        data = db.fetchall("""
            SELECT p.user_id, u.email, p.lab_id
            FROM Presenca p
            INNER JOIN User_Lab u
              ON p.user_id = u.user_id
            WHERE presente = 1;""")

        events = []
        for d in data:
            events += [(now, d[0], d[2], "OUT")]
            emails += [d[1]]

        db.execute("""
            UPDATE Presenca
            SET presenca = 0;""")

        now = int(datetime.now().timestamp())
        db.executemany("""
            INSERT  INTO Log_Presenca
            (data, user_id, lab_id, evento)
            VALUES (?, ?, ?, ?);""",
            events)
        return emails

    def obter_intervalo_parser(lab_id):
        return db.fetchone("""
            select intervalo_parser
            from lab
            where lab_id = ?;""", (lab_id,))

    def obter_intervalo_arduino(lab_id):
        return db.fetchone("""
            select intervalo_arduino
            from lab
            where lab_id = ?;""", (lab_id,))
