from . import db

class MyDenox:
    def __init__(self, epoch, status, slug):
        self.ultima_atualizacao = epoch
        self.status = status
        self.slug = slug

    def log(epoch, status, slug):
        db.execute("""
            INSERT INTO Log_MyDenox
            (data, evento, slug)
            VALUES (?, ?, ?);""", (epoch, status, slug))

    def ultima_atualizacao():
        data = db.fetchone("""
            SELECT data, evento, slug
            FROM Log_MyDenox
            ORDER by data DESC;""")
        if data is not None:
            return MyDenox(*data)
