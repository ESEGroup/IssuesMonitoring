from ..models import Anomalia

def obter_anomalias(lab_id):
    return Anomalia.obter_do_lab(lab_id)

def resolver_anomalia(id_anomalia, user_id, descricao_acao):
    return Anomalia.registrar_resolucao(id_anomalia, descricao_acao,
                                        user_id)
