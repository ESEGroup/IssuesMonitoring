from datetime import datetime, timedelta
from time import sleep
from ..common.mail import send_email
from ..models import (Laboratorio, Evento, UsuarioLab, MyDenox,
                      AdministradorSistema)

def log_mydenox(epoch, message, slug):
    MyDenox.log(epoch, message, slug)

def obter_intervalo_parser():
    return Laboratorio.obter_intervalo_parser()

def registrar_presenca(eventos_dict):
    if len(eventos_dict) > 0:
        eventos = []
        user_ids = []
        for e in eventos_dict:
            try:
                user_ids += [e['user_id']]
                eventos += [Evento(e['epoch'],
                                   e['event'],
                                   e['user_id'],
                                   e.get('lab_id'))]
            except KeyError:
                pass
        UsuarioLab.registrar_presenca(eventos)

        registered_user_ids = UsuarioLab.user_ids_registradas(user_ids)
        unregistered_user_ids = set(user_ids) - set(registered_user_ids)
        enviar_email_usuarios_nao_cadastrados(unregistered_user_ids)
    return obter_intervalo_parser()

def enviar_email_usuarios_nao_cadastrados(user_ids):
    if len(user_ids) == 0:
        return

    admins = AdministradorSistema.obter_administradores()
    emails = [a.email for a in admins]

    plural = "s" if len(user_ids) > 1 else ""
    subject = "Usuário{0} cadastrado{0} no MyDenox não cadastrado{0} no Sistema".format(plural)
    msg_content = "Foi recebido log de presença/saída no sistema MyDenox referente ao{0} usuário{0} {1}, porém não há cadastro dele{0} no Sistema.\nPor favor cadastre-os em seus respectivos laboratórios.".format(
            plural,
            ", ".join(list(user_ids)))
    send_email(subject, msg_content, emails)

def enviar_email_presenca_zerada(emails):
    msg_content = """
Caro usuário,
Você está recebendo essa mensagem pois se encontra marcado como 'presente' no laboratório.
Informamos que às 00:00h de hoje, todos os logs de presença foram reiniciados.
Caso ainda se encontre no laboratório, pedimos que renove seu registro de presença.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

    send_email("Alerta de Reset de presenças",
              msg_content,
              emails)

def reset_presencas_meia_noite():
    while True:
        hoje = datetime.today()
        proxima_execucao = datetime(
            day   = hoje.day,
            month = hoje.month,
            year  = hoje.year) + timedelta(days=1)
        delta_t = proxima_execucao - hoje
        segundos_ate = delta_t.seconds + 1
        sleep(segundos_ate)
        emails = Laboratorio.reset_lista_presenca()
        enviar_email_presenca_zerada(emails)

def ultima_atualizacao_mydenox():
    return MyDenox.ultima_atualizacao()

def ultima_atualizacao_parser():
    return Laboratorio.ultima_atualizacao_parser()

def registrar_log_parser():
    Laboratorio.registrar_log_parser()
    return Laboratorio.obter_intervalo_parser()
