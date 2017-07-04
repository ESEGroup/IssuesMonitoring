from ..models import Anomalia, UsuarioLab, AdministradorSistema, Laboratorio, UsuarioSistema
from ..common.mail import send_email

def obter_anomalia(id):
    return Anomalia.obter(id)

def obter_anomalias(lab_id):
    return Anomalia.obter_do_lab(lab_id)

def obter_anomalias_resolvidas_dia(lab_id, dia):
    return Anomalia.obter_do_lab(lab_id, True, dia)

def resolver_anomalia(id_anomalia, descricao_acao, user_id):
    return Anomalia.registrar_resolucao(id_anomalia, descricao_acao,
                                        user_id)
def enviar_email_acao_realizada(lab_id, descricao_acao, tipo_anomalia, user_id):
    presentes = UsuarioLab.presentes(lab_id)
    admins = AdministradorSistema.obter_administradores()
    emails = [a.email for a in admins]
    emails += [p.email for p in presentes]
    lab = Laboratorio.obter(lab_id)
    if lab is not None:
        nome_laboratorio = lab.nome
    else:
        nome_laboratorio = "-"
    u = UsuarioSistema.obter(user_id)
    if u is not None:
        nome_usuario = u.nome
    else:
        nome_usuario = "-"

    subject = "Ação realizada no laboratório {}".format(nome_laboratorio)
    msg_content = """O usuário {} solucionou a anomalia referente a {}\n\n Ação: {}""".format(
                    nome_usuario,
                    tipo_anomalia,
                    descricao_acao)
    send_email(subject, msg_content, emails)

def data_proxima_anomalia_resolvida(lab_id, dia):
    return Anomalia.data_proxima_resolvida(lab_id, dia)

def data_anomalia_resolvida_anterior(lab_id, dia):
    return Anomalia.data_resolvida_anterior(lab_id, dia)

def registrar_anomalia(slug):
    if Anomalia.nao_repetida(slug)[1]:
        Anomalia.registrar_anomalia(None, slug)
