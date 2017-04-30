from datetime import datetime, timedelta
from time import sleep
from ..common.mail import send_email
from ..models import Laboratorio, Evento, UsuarioLab

def obter_intervalo_parser():
    return Laboratorio.obter_intervalo_parser()

def registrar_presenca(dict_eventos):
    eventos = []
    for e in dict_eventos:
        try:
            eventos += [Evento(e['epoch'],
                               e['event'],
                               e['user_id'])]
        except KeyError:
            pass
    UsuarioLab.registrar_presenca(eventos)

def enviar_email_presenca_zerada(emails):
    msg_content = """
Caro usuário,
Você está recebendo essa mensagem pois se encontra marcado como 'presente' no laboratório.
Informamos que às 00:00h de hoje, todos os logs de presença foram reiniciados.
Caso ainda se encontre no laboratório, pedimos que renove seu registro de presença.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

    send_mail("Alerta de Reset de presenças",
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
