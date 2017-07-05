from . import db
from datetime import datetime
from .usuario_lab import UsuarioLab

class Anomalia:
    def __init__(self, tipo, lab_id, descricao, data, resolvido, id,
                 data_resolucao, acao, nome_autor_resolucao, equip_id,
                 equip_nome, equip_MAC, valor, valor_limite):
        self.tipo = tipo
        if None in [valor, valor_limite]:
            args = []
        elif equip_id is None:
            args = [valor, valor_limite]
        else:
            args = [valor, "{} ({})".format(equip_nome, equip_MAC), valor_limite]
        self.descricao = descricao.format(*args)
        self.data_anomalia = data
        self.lab_id = lab_id
        self.resolvido = resolvido
        self.id = id
        self.data_resolucao = data_resolucao
        self.acao = acao
        self.nome_autor_resolucao = nome_autor_resolucao
        self.equip_id = equip_id

    def obter(id):
        data = db.fetchone("""SELECT a.tipo_anomalia, log.lab_id, a.descricao_anomalia,
                                     log.data, log.resolvido, log.id,
                                     r.data, r.descricao_acao, u.nome,
                                     log.equip_id, e.nome, e.end_mac, log.valor, log.valor_limite
                              FROM Log_Anomalias log
                              INNER JOIN Anomalias a
                                ON a.slug = log.slug_anomalia
                              LEFT JOIN Log_Acoes r
                                ON r.id_log_anomalia = log.id
                              LEFT JOIN User_Sys u
                                ON u.user_id = r.autor
                              LEFT JOIN Equip e
                                ON e.equip_id = log.equip_id
                              WHERE log.id = ?;""",
                              (id,))
        if data is not None:
            return Anomalia(*data)

    def obter_do_lab(lab_id, resolvido=False, dia=None):
        args = [lab_id, int(resolvido)]
        if dia is not None:
            args += [dia, dia + 60 * 60 * 24]
        query = """SELECT a.tipo_anomalia, log.lab_id, a.descricao_anomalia,
                          log.data, log.resolvido, log.id,
                          r.data, r.descricao_acao, u.nome,
                          log.equip_id, e.nome, e.end_mac, log.valor,
                          log.valor_limite
                   FROM Log_Anomalias log
                   INNER JOIN Anomalias a
                     ON a.slug = log.slug_anomalia
                   LEFT JOIN Log_Acoes r
                     ON r.id_log_anomalia = log.id
                   LEFT JOIN User_Sys u
                     ON u.user_id = r.autor
                   LEFT JOIN Equip e
                     ON e.equip_id = log.equip_id
                   WHERE (log.lab_id = ?
                          OR log.lab_id IS NULL)
                          AND log.resolvido = ? {};""".format(
                              "AND r.data > ? AND r.data < ?"
                              if dia is not None else "")
        data = db.fetchall(query, args)
        return [Anomalia(*d) for d in data]

    def registrar_anomalia(lab_id, slug_anomalia, valor=None, valor_limite=None, equip_id=None):
        db.execute("""
            INSERT INTO Log_Anomalias
            (data, lab_id, slug_anomalia, resolvido, equip_id, valor, valor_limite)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (int(datetime.now().timestamp()),
             lab_id,
             slug_anomalia,
             0,
             equip_id,
             int(valor),
             int(valor_limite)))

    def registrar_resolucao(id_log, descricao_acao, id_autor):
        db.execute("""
            INSERT INTO Log_Acoes
            (data, id_log_anomalia, descricao_acao, autor)
            VALUES (?, ?, ?, ?);""", (int(datetime.now().timestamp()), id_log, descricao_acao, id_autor))
        db.execute("""
            UPDATE Log_Anomalias
            SET resolvido = ?
            WHERE id = ?""", (1, id_log))

    def nao_repetida(slug, anti_slug=None):
        if anti_slug is None:
            anti_slug = slug
        data = db.fetchone("""
            SELECT slug_anomalia, id
            FROM Log_Anomalias
            WHERE resolvido = ?
                  AND (slug_anomalia = ?
                       OR slug_anomalia = ?)
            ORDER BY data DESC;""",
            (0, slug, anti_slug))
        if data is not None:
            return data[1], data[0] != slug
        return [None, True]

    def atualizar_valor(id, valor, data):
        db.execute("""
            UPDATE Log_Anomalias
            SET valor = ?,
                data = ?
            WHERE id = ?;""", (valor, data, id))

    def data_proxima_resolvida(lab_id, dia):
        dia_dt = datetime.fromtimestamp(dia)
        dia = int(datetime(day=dia_dt.day,
                           month=dia_dt.month,
                           year=dia_dt.year,
                           hour=23,
                           minute=59,
                           second=59).timestamp())
        data = db.fetchone("""SELECT r.data
                           FROM Log_Anomalias log
                           INNER JOIN Log_Acoes r
                             ON r.id_log_anomalia = log.id
                           WHERE log.lab_id = ?
                                 AND log.resolvido = ?
                                 AND r.data > ?
                           ORDER BY r.data ASC;""",
                           (lab_id,
                            True,
                            dia))
        if data is not None:
            return data[0]
        return dia_dt.timestamp()

    def data_resolvida_anterior(lab_id, dia):
        data = db.fetchone("""SELECT r.data
                           FROM Log_Anomalias log
                           INNER JOIN Log_Acoes r
                             ON r.id_log_anomalia = log.id
                           WHERE log.lab_id = ?
                                 AND log.resolvido = ?
                                 AND r.data < ?
                           ORDER BY r.data DESC;""",
                           (lab_id,
                            True,
                            dia))
        if data is not None:
            return data[0]
        return dia
