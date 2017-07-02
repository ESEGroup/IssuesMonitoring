from . import db

class Sistema:
    def obter_data_inicio():
        data = db.fetchone("""
            SELECT ultima_analise
            FROM Sistema;""")
        if data is not None:
            return data[0]
        return 0

    def definir_data_inicio(data):
        db.execute("""
            UPDATE Sistema
            SET ultima_analise = ?;""",
            (data,))

    def obter_intervalo_parser():
        pass

    def definir_intervalo_parser():
        pass
