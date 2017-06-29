from . import db

class MyDenox:
    def __init__(self, epoch, status):
        self.epoch = epoch
        self.status = status

    def log(epoch, status):
        db.execute("""
            INSERT INTO Log_MyDenox
            (data, evento)
            VALUES (?, ?);""", (epoch, status))

    def ultima_atualizacao():
        data = db.fetchone("""
            SELECT epoch, evento
            FROM Log_MyDenox
            ORDER by epoch DESC;""")
        if data is not None:
            return MyDenox(*data)

