from . import db

class Equipamento:
    def __init__(self, lab_id, nome, descricao, MAC, id = None):
        self.id        = id
        self.nome      = nome
        self.descricao = descricao
        self.lab_id    = lab_id
        self.MAC       = MAC

    def cadastrar(self):
        pass

    def remover(_id):
        db.execute("""
            DELETE FROM Equip
            WHERE equip_id = ?;""", (_id,))

    def editar(self):
        pass

    def obter(id):
        pass

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

    def obter_medidas_entre_tempos_equip(tempo_inicio, tempo_final, equip_id):
        data = db.fetchall("""
            SELECT data, temp
            FROM Log_Equip
            WHERE equip_id = ?
                  AND data >= ?
                  AND data < ?
            ORDER BY data ASC;""", (equip_id, tempo_inicio, tempo_final))
        return data
