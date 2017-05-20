from . import db

class Equipamento:
    def __init__(self, lab_id, temp_min, temp_max, MAC, id = None):
        self.id       = id
        self.lab_id   = lab_id
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.MAC      = MAC

    def obter_medidas(_id):
        pass

    def registrar_medidas(_id, temperatura, umidade, luminosidade):
        db.execute("""
            INSERT INTO Log_Lab
            (lab_id, temp_min, temp_max, end_mac)
            VALUES (?, ?, ?, ?)""",)
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
