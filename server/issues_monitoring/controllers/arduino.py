from ..models import Laboratorio, Evento, UsuarioLab, Arduino

def registrar_medidas(json):
    medidas = []
    dict_medidas = {}
    try:
        MAC = json["MAC"]
        dict_medidas = json["data"]
        all_mac = listar_todos_mac_arduino()
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
            medidas += [Medida(m['epoch'],
                               m['event'],
                               m['user_id'])]
        except KeyError:
            pass
    UsuarioLab.registrar_presenca(medidas)
    return True

def listar_todos_mac_arduino():
    data = Arduino.listar_todos()
    mac_arduinos = []
    for a in data:
        mac_arduinos += [a[len(a)-1]]
    return str(mac_arduinos)
