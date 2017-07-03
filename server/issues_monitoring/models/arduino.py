from . import db
from .equipamento import Equipamento

class Arduino(Equipamento):
    def cadastrar(self):
        db.execute("""
            INSERT INTO Equip
            (nome, descricao, lab_id, end_mac)
            VALUES (?, ?, ?, ?)""",
            (self.nome,
             self.descricao,
             self.lab_id,
             self.MAC))

    def editar(self):
        db.execute("""
          UPDATE Equip
          SET nome = ?,
              descricao = ?,
              lab_id = ?,
              end_mac = ?
          WHERE equip_id = ?""",
          (self.nome,
           self.descricao,
           self.lab_id,
           self.MAC,
           self.id))

    def obter(id):
        data = db.fetchone("""SELECT lab_id, nome, descricao, end_mac, equip_id
                              FROM Equip
                              WHERE equip_id = ?;""", (id,))
        if data is not None:
            return Arduino(*data)

    def obter_todos():
        data = db.fetchall("""
            SELECT lab_id, nome, descricao, end_mac, equip_id
            FROM Equip
            WHERE parent_id = 0;""")
        return [Arduino(*d) for d in data]

    def obter_do_lab(lab_id):
        data = db.fetchall("""
            SELECT lab_id, nome, descricao, end_mac, equip_id
            FROM Equip
            WHERE parent_id = 0
                  AND lab_id = ?;""", (lab_id,))
        return [Arduino(*d) for d in data]
