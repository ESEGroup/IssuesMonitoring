from . import db

class Anomalia:
    def __init__(self, tipo, lab_id, descricao, data, resolvido, id,
                 data_resolucao, acao, nome_autor_resolucao):
        self.tipo = tipo
        self.descricao = descricao
        self.data_anomalia = data
        self.lab_id = lab_id
        self.resolvido = resolvido
        self.id = id
        self.data_resolucao = data_resolucao
        self.acao = acao
        self.nome_autor_resolucao = nome_autor_resolucao

    def obter_do_lab(lab_id):
        data = db.fetchall("""SELECT a.tipo_anomalia, log.lab_id, a.descricao_anomalia,
                                     log.data, log.resolvido, log.id,
                                     r.data, r.descricao_acao, u.nome
                              FROM Log_Anomalias log
                              INNER JOIN Anomalias a
                                ON a.slug = log.slug_anomalia
                              LEFT JOIN Log_Acoes r
                                ON r.id_log_anomalia = log.id
                              LEFT JOIN User_Lab u
                                ON u.user_id = r.autor
                              WHERE log.lab_id = ?
                                    AND log.resolvido = ?;""",
                              (lab_id, False))
        print (data)
        return [Anomalia(*d) for d in data]

    def registrar_anomalia(lab_id, slug_anomalia):
        db.execute("""
            INSERT INTO Log_Anomalias
            (data, lab_id, slug_anomalia, resolvido)
            VALUES (?, ?, ?, ?)""",
            (int(datetime.now().timestamp()),
             lab_id,
             slug_anomalia,
             0))

    def registrar_resolucao(id_log, descricao_acao, id_autor):
        db.execute("""
            INSERT INTO Log_Acoes
            (data, id_log_anomalia, descricao_acao, autor)
            VALUES (?, ?, ?, ?);""", (id_log, descricao_acao, id_autor))
        db.execute("""
            UPDATE Log_Anomalias
            SET resolvido = ?
            WHERE id = ?""", (1, id_log))
