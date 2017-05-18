from ..models import Laboratorio, Evento, UsuarioLab, Arduino

def registrar_medidas(json):
    medidas = []
    dict_medidas = {}
    try:
        MAC = json["MAC"]
        #Pegar
    except KeyError:
        print("MAC não encontrado")
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

def listar_todos_mac_arduino():
    print ("ENTROU LISTAR TODOS")
    data = Arduino.listar_todos()
    print ("LISTOU TODOS!!!!!")
    mac_arduinos = []
    for a in data:
        mac_arduinos += [*a[len(*a)-1]]

    return str(mac_arduinos)
