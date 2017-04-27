from ..models import Laboratorio, Evento, UsuarioLab, Equipamento

def obter_informacoes_lab():
    return Laboratorio.obter_informacoes()

def atualizar_informacoes_lab(user_id, nome, endereco, intervalo_parser, intervalo_arduino):
    return Laboratorio.editar_laboratorio(user_id,
                                          nome,
                                          endereco,
                                          intervalo_parser,
                                          intervalo_arduino)

def registrar_equipamento(temp_min, temp_max, MAC):
    equipamento = Equipamento(temp_min, temp_max, MAC)
    return equipamento.cadastrar()

def remover_equipamento(_id):
    return Equipamento.remover(_id)

