from ..models import (Laboratorio, Evento, UsuarioLab, Equipamento,
                      ZonaConforto)

def cadastro_laboratorio(nome, endereco, intervalo_parser,
                          intervalo_arduino, temp_min, temp_max,
                          umid_min, umid_max, lumin_min,
                          lumin_max):
    zona_de_conforto = ZonaConforto(temp_min,
                                    temp_max,
                                    umid_min,
                                    umid_max,
                                    lumin_min,
                                    lumin_max)
    zona_de_conforto.cadastrar()

    laboratorio = Laboratorio(nome,
                              endereco,
                              intervalo_parser,
                              intervalo_arduino,
                              zona_de_conforto)
    laboratorio.cadastrar()

def obter_informacoes_labs():
    return Laboratorio.obter_informacoes()

def atualizar_informacoes_lab(lab_id, nome, endereco, intervalo_parser,
                              intervalo_arduino, temp_min, temp_max,
                              umid_min, umid_max, lumin_min,
                              lumin_max):
    zona_conforto = ZonaConforto(temp_min,
                                 temp_max,
                                 umid_min,
                                 umid_max,
                                 lumin_min,
                                 lumin_max,
                                 lab_id)
    zona_conforto.editar()
    laboratorio = Laboratorio(nome,
                              endereco,
                              intervalo_parser,
                              intervalo_arduino,
                              id=lab_id)
    laboratorio.editar()

def obter_laboratorios():
    return Laboratorio.obter_todos()

def cadastro_equipamento(lab_id, temp_min, temp_max, MAC):
    equipamento = Equipamento(lab_id, temp_min, temp_max, MAC)
    equipamento.cadastrar()

def remover_equipamento(_id):
    Equipamento.remover(_id)
