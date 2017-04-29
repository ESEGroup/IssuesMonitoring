from datetime import datetime
from time import sleep
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
    pass

def reset_presencas_meia_noite():
    while True:
        hoje = datetime.today()
        proxima_execucao = hoje.replace(day=hoje.day+1,
                                        hour=0,
                                        minute=0,
                                        second=0,
                                        microsecond=0)
        delta_t = proxima_execucao - hoje
        segundos_ate = delta_t.seconds + 1
        sleep(segundos_ate)
        emails = Laboratorio.reset_lista_presenca()
        enviar_email_presenca_zerada(emails)
