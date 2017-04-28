from ..models import Laboratorio, Evento, UsuarioLab, Equipamento

def obter_informacoes_labs():
    return Laboratorio.obter_informacoes()

def atualizar_informacoes_lab(nome, endereco, intervalo_parser, intervalo_arduino):
    return Laboratorio.editar_laboratorio(nome,
                                          endereco,
                                          intervalo_parser,
                                          intervalo_arduino)

def listar_laboratorios():
    return Laboratorio.listar_todos()

def cadastrar_equipamento(lab_id, temp_min, temp_max, MAC):
    equipamento = Equipamento(lab_id, temp_min, temp_max, MAC)
    return equipamento.cadastrar()

def remover_equipamento(_id):
    return Equipamento.remover(_id)
