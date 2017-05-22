from . import db
import sqlite3

class Arduino:
    def __init__(self, lab_id, equip_id, MAC, id = None):
        self.id       = id
        self.lab_id   = lab_id
        self.equip_id = equip_id
        self.MAC      = MAC

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
