from . import db

class MyDenox:
    def __init__(self, epoch, status):
        self.ultima_atualizacao = epoch
        self.status = status

    def log(epoch, status):
        db.execute("""
            INSERT INTO Log_MyDenox
            (data, evento)
            VALUES (?, ?);""", (epoch, status))

    def ultima_atualizacao():
        data = db.fetchone("""
            SELECT data, evento
            FROM Log_MyDenox
            ORDER by data DESC;""")
        if data is not None:
            return MyDenox(*data)
