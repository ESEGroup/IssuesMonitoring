from ..models import Laboratorio, Evento, UsuarioLab, Medida_Lab, Medida_Equip, Equipamento

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

        except KeyError:
            pass

    return True

def listar_todos_mac_arduino():
    data         = Equipamento.listar_todos_arduinos()
    mac_arduinos = []

    for a in data:
        mac_arduinos += [a[5]]
    return str(mac_arduinos)

def listar_todos_arduinos():
    data         = Equipamento.listar_todos_arduinos()
    arduinos     = []
    for a in data:
        arduinos += [Equipamento(*a)]
    return arduinos

def ultima_atualizacao_arduino(id):
    return Laboratorio.ultima_atualizacao_arduino(id)
