from ..models import (Laboratorio, Evento, UsuarioLab, Equipamento,
                      ZonaConforto)
from ..models.check_condicoes import check_for_forgotten_lights, check_for_abnormal_humidity, check_for_abnormal_temperature, check_for_equipment_temperature, get_equip_ids, get_data_graphic
from threading import Thread
from time import sleep
import json

def cadastro_laboratorio(nome, endereco, intervalo_parser,
                          intervalo_arduino, temp_min, temp_max,
                          umid_min, umid_max):
    zona_de_conforto = ZonaConforto(temp_min,
                                    temp_max,
                                    umid_min,
                                    umid_max)
    zona_de_conforto.cadastrar()

    laboratorio = Laboratorio(nome,
                              endereco,
                              intervalo_parser,
                              intervalo_arduino,
                              zona_de_conforto)
    laboratorio.cadastrar()

def remover_laboratorio(id):
    Laboratorio.remover(id)

def obter_informacoes_labs():
    return Laboratorio.obter_informacoes()

def atualizar_zona_de_conforto(temp_min, temp_max, umid_min, umid_max, lab_id):
    zona_conforto = ZonaConforto(temp_min,
                                 temp_max,
                                 umid_min,
                                 umid_max,
                                 lab_id)
    zona_conforto.editar()

def atualizar_informacoes_lab(lab_id, nome, endereco, intervalo_parser,
                              intervalo_arduino):
    laboratorio = Laboratorio(nome,
                              endereco,
                              intervalo_parser,
                              intervalo_arduino,
                              id=lab_id)
    laboratorio.editar()

def obter_laboratorios():
    return Laboratorio.obter_todos()

def obter_laboratorio(id):
    return Laboratorio.obter(id)

def cadastro_equipamento(lab_id, temp_min, temp_max, MAC):
    equipamento = Equipamento(lab_id, temp_min, temp_max, MAC)
    equipamento.cadastrar()

def remover_equipamento(_id):
    Equipamento.remover(_id)

def obter_zona_de_conforto(id):
    return ZonaConforto.obter(id)

def obter_laboratorios_id():
    return Laboratorio.obter_todos_ids()

def checar_condicoes_no_intervalo():
    #since we have multiple labs, we have multiple threads
    lab_ids = obter_laboratorios_id() #gets all lab ids
    threadsCondicoes = []
    for i in range (len(lab_ids)): 
        threadsCondicoes.append(Thread(target=check_condicoes_ambiente, args=(lab_ids[i],)))
        threadsCondicoes[i].daemon = True
        threadsCondicoes[i].start()     

def check_condicoes_ambiente(lab_id):
  while (True):
      checkInterval = 1. #TODO: na vdd pegar do BD(n tem ainda, entao n sei como)
      checkIntervalSeconds = checkInterval*60. #transform to seconds
      sleep(checkIntervalSeconds)

      #do the checks(FOR EACH LAB)
      check_for_forgotten_lights(lab_id)
      check_for_abnormal_temperature(lab_id)
      check_for_abnormal_humidity(lab_id)
      
      #get equips from query
      equips = get_equip_ids(lab_id)

      for eq in equips:
        check_for_equipment_temperature(eq,lab_id)            

def get_data_log(chart_type, start_date, end_date, lab_id):
  json_string = json.dumps(get_data_graphic(chart_type, start_date, end_date, lab_id))
  return json_string


# def get_log_presence_list(date, lab_id):
#   #Date of today, start of query
#   dateToday = date
#   #end of today, end of query
#   dateTomorrow = date+24*60*60. -1. 
#   json_string = json.dumps(get_presence_data(dateToday, dateTomorrow, lab_id))   
#   return json_string
