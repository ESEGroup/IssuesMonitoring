from . import db

class Equipamento:
    def __init__(self, lab_id, nome, descricao, temp_min, temp_max, MAC, parent_id, id = None):
        self.id        = id
        self.nome      = nome
        self.descricao = descricao
        self.lab_id    = lab_id
        self.temp_min  = temp_min
        self.temp_max  = temp_max
        self.MAC       = MAC
        self.parent_id = parent_id

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

    def remover(_id):
        db.execute("""
            DELETE FROM Equip
            WHERE equip_id = ?;""", (_id,))

    def obter(id):
        data = db.fetchone("""SELECT lab_id, nome, descricao, temp_min, temp_max, end_mac, parent_id, equip_id
                              FROM Equip
                              WHERE equip_id = ?;""", (id,))
        if data is not None:
            return Equipamento(*data)

    def nome(id):
        data = db.fetchone("""SELECT nome
                              FROM Equip
                              WHERE equip_id = ?;""", (id,))
        if data is not None:
            return data[0]
        return "-"

    def obter_medida(id, data_inicio, data_final):
        data = db.fetchone("""
        SELECT temp_min, temp, temp_max, nome
        FROM Log_Equip log
        INNER JOIN Equip e
          ON log.equip_id = e.equip_id
        WHERE e.equip_id = ?
              AND log.data > ?
              AND log.data <= ?
        ORDER BY log.data DESC""", (id,
                                    data_inicio,
                                    data_final))

        if data is not None:
            return data
        return [0, 0, 0, ""]

    def listar_todos_arduinos():
        data = db.fetchall("""
            SELECT lab_id, nome, descricao, temp_min, temp_max, end_mac, parent_id, equip_id
            FROM Equip
            WHERE parent_id = 0;""")
        return data
