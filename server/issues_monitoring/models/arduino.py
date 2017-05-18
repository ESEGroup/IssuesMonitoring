from . import db

class Arduino:
    def __init__(self, lab_id, equip_id, MAC, id = None):
        self.id       = id
        self.lab_id   = lab_id
        self.equip_id = equip_id
        self.MAC      = MAC

    #CHANGE!
    def registrar_medidas_lab(lab_id, temperatura, umidade, luminosidade):
        db.execute("""
            INSERT INTO Log_Lab
            (lab_id, temp_min, temp_max, end_mac)
            VALUES (?, ?, ?, ?)""",)
        data_registro = int(datetime.now().timestamp())

    #CHANGE!
    def registrar_medidas_equip(lab_id, temperatura, umidade, luminosidade):
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

    def listar_todos():
        data = db.fetchall("""
            SELECT *
            FROM Arduino;""")
        return data
