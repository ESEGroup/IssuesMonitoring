from . import db

class Equipamento:
    def __init__(self, nome, descricao, lab_id, temp_min, temp_max, MAC, id = None):
        self.id       = id
        self.nome = nome
        self.descricao = descricao
        self.lab_id   = lab_id
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.MAC      = MAC

    def cadastrar(self):
        db.execute("""
            INSERT INTO Equip
            (nome, descricao, lab_id, temp_min, temp_max, end_mac)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (self.nome,
             self.descricao,
             self.lab_id,
             self.temp_min,
             self.temp_max,
             self.MAC))

    def remover(_id):
        db.execute("""
            DELETE FROM Equip
            WHERE equip_id = ?;""", (_id,))

    def obter(id):
        data = db.fetchone("""SELECT nome, descricao, lab_id, temp_min, temp_max, end_mac, equip_id
                              FROM Equip
                              WHERE equip_id = ?;""", (id,))
        if data is not None:
            return Equipamento(*data)
