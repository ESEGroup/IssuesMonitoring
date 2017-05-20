from . import db

class ZonaConforto:
    def __init__(self, temp_min, temp_max, umidade_min, umidade_max,
                 lab_id = None, id = None):
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.umidade_min = umidade_min
        self.umidade_max = umidade_max
        self.lab_id = lab_id
        self.id = id

    def cadastrar(self):
        args = (self.temp_min,
                self.temp_max,
                self.umidade_min,
                self.umidade_max)
        self.id = db.execute("""
            INSERT INTO Zona_de_Conforto_Lab
            (temp_min, temp_max, umid_min, umid_max)
            VALUES (?, ?, ?, ?);""",
            args,
            return_id=True)

    def editar(self):
        db.execute("""
            UPDATE Zona_de_Conforto_Lab
            SET temp_min = ?,
                temp_max = ?,
                umid_min = ?,
                umid_max = ?
            WHERE zona_conforto_id in (SELECT zona_conforto_id
                                       FROM Lab
                                       WHERE lab_id = ?);""",
            (self.temp_min,
             self.temp_max,
             self.umidade_min,
             self.umidade_max,
             self.lab_id))
