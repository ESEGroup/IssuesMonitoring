from ..models import Laboratorio, Evento, UsuarioLab

def obter_intervalo_parser():
    return Laboratorio.obter_invervalo_parser()

def registrar_presenca(dict_eventos):
    eventos = []
    for e in dict_eventos:
        try:
            eventos += [Evento(e['epoch'],
                               e['event'],
                               e['user_id'])]
        except KeyError:
            pass
    return UsuarioLab.registrar_presenca(eventos)
