from . import db
from datetime import datetime
from .usuario_lab import UsuarioLab
from .equipamento import Equipamento

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
                              LEFT JOIN User_Lab u
                                ON u.user_id = r.autor
                              LEFT JOIN Equip e
                                ON e.equip_id = log.equip_id
                              WHERE log.id = ?;""",
                              (id,))
        if data is not None:
            return Anomalia(*data)

    def obter_do_lab(lab_id):
        data = db.fetchall("""SELECT a.tipo_anomalia, log.lab_id, a.descricao_anomalia,
                                     log.data, log.resolvido, log.id,
                                     r.data, r.descricao_acao, u.nome,
                                     log.equip_id, e.nome, e.end_mac, log.valor,
                                     log.valor_limite
                              FROM Log_Anomalias log
                              INNER JOIN Anomalias a
                                ON a.slug = log.slug_anomalia
                              LEFT JOIN Log_Acoes r
                                ON r.id_log_anomalia = log.id
                              LEFT JOIN User_Lab u
                                ON u.user_id = r.autor
                              LEFT JOIN Equip e
                                ON e.equip_id = log.equip_id
                              WHERE log.lab_id = ?
                                    AND log.resolvido = ?;""",
                              (lab_id, False))
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
             valor,
             valor_limite))

    def registrar_resolucao(id_log, descricao_acao, id_autor):
        db.execute("""
            INSERT INTO Log_Acoes
            (data, id_log_anomalia, descricao_acao, autor)
            VALUES (?, ?, ?, ?);""", (int(datetime.now().timestamp()), id_log, descricao_acao, id_autor))
        db.execute("""
            UPDATE Log_Anomalias
            SET resolvido = ?
            WHERE id = ?""", (1, id_log))

    def nao_resolvida(slug, anti_slug=None):
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
        return data[1], data is not None and data[0] == slug

    def atualizar_valor(id, valor, data):
        db.execute("""
            UPDATE Log_Anomalia
            SET valor = ?,
                data = ? 
            WHERE id = ?;""", (valor, id, data))
