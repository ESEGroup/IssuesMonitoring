from ..models import Laboratorio, Evento, UsuarioLab, Arduino, Medida_Lab, Medida_Equip
from ..models.check_condicoes import check_for_forgotten_lights, check_for_abnormal_humidity, check_for_abnormal_temperature, check_for_equipment_temperature
import sqlite3
import json

def registrar_medidas(j):
    dict_medidas = {}
    try:
        MAC          = j["MAC"]
        dict_medidas = j["dados"]
        lab_id       = j["lab_id"]
        all_mac      = listar_todos_mac_arduino()
        if MAC not in all_mac:
            print ("MAC não cadastrado")
            return False
    except KeyError:
        print("MAC não encontrado no JSON")
        return False
    except:
        print("Erro não esperado")
        return False

    for m in dict_medidas:
        try:
            equips   = m['equipamentos']
            l_equips = []

            for eq in equips:
                l_equips += [Medida_Equip(eq['id'], eq['temperatura'])]
            medida_lab = Medida_Lab(lab_id,
                                    m['luz']==1,
                                    m['umidade'],
                                    m['sensacao_termica'],
                                    l_equips)
            Laboratorio.registrar_medidas(medida_lab)
            check_for_forgotten_lights(lab_id)
            check_for_abnormal_temperature(lab_id)
            check_for_abnormal_humidity(lab_id)
            for eq in l_equips:
                check_for_equipment_temperature(eq.equip_id,lab_id)

        except KeyError:
            pass

    return True

def listar_todos_mac_arduino():
    data         = Arduino.listar_todos()
    mac_arduinos = []

    for a in data:
        mac_arduinos += [a[len(a)-1]]
    return str(mac_arduinos)
