from ..models import Laboratorio, Evento, UsuarioLab

def obter_informacoes_lab():
    return Laboratorio.obter_informacoes()

def atualizar_informacoes_lab(user_id, nome, endereco, intervalo_parser, intervalo_arduino):
    return Laboratorio.editar_laboratorio(user_id,
                                          nome,
                                          endereco,
                                          intervalo_parser,
                                          intervalo_arduino)
