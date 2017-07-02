from . import db
from .equipamento import Equipamento

class Computador(Equipamento):
    def __init__(self, lab_id, nome, descricao, temp_min, temp_max, MAC,
                 parent_id, id = None, nome_arduino = None, MAC_arduino = None):
        super().__init__(lab_id, nome, descricao, MAC, id)
        self.temp_min  = temp_min
        self.temp_max  = temp_max
        self.parent_id = parent_id
        self.nome_arduino = nome_arduino
        self.MAC_arduino = MAC_arduino or ""

    def cadastrar(self):
        db.execute("""
            INSERT INTO Equip
            (nome, descricao, lab_id, temp_min, temp_max, end_mac, parent_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (self.nome,
             self.descricao,
             self.lab_id,
             self.temp_min,
             self.temp_max,
             self.MAC,
             self.parent_id))

    def editar(self):
        db.execute("""
          UPDATE Equip
          SET nome = ?,
              descricao = ?,
              lab_id = ?,
              temp_min = ?,
              temp_max = ?,
              end_mac = ?,
              parent_id = ?
          WHERE equip_id = ?""",
          (self.nome,
           self.descricao,
           self.lab_id,
           self.temp_min,
           self.temp_max,
           self.MAC,
           self.parent_id,
           self.id))

    def obter(id):
        data = db.fetchone("""SELECT lab_id, nome, descricao, temp_min, temp_max, end_mac, parent_id, equip_id
                              FROM Equip
                              WHERE equip_id = ?;""", (id,))
        if data is not None:
            return Computador(*data)

    def obter_do_lab(lab_id):
        data = db.fetchall("""
            SELECT e.lab_id, e.nome, e.descricao, e.temp_min, e.temp_max, e.end_mac, e.parent_id, e.equip_id,
                   a.nome, a.end_mac
            FROM Equip as e
            INNER JOIN Equip a
              ON a.equip_id = e.parent_id
            WHERE e.lab_id = ?;""", (lab_id,))

        return [Computador(*d) for d in data]
