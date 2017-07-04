from flask import session
from datetime import datetime
from random import choice
from string import ascii_letters, digits
from .filters import *
from .. import Config

def autenticado():
    tem_user_id = session.get('id') is not None

    expira = session.get('expiration') or 0
    nao_expirado = expira > datetime.today().timestamp()
    _autenticado = tem_user_id and nao_expirado
    if _autenticado:
        now = int(datetime.today().timestamp())
        session['expiration'] = now + Config.session_duration
    return nao_expirado and tem_user_id

def admin_autenticado():
    return autenticado() and session.get('admin') == True

def random_string(n):
    alfabeto = ascii_letters + digits
    return ''.join(choice(alfabeto) for i in range(n))

def hoje():
    agora = datetime.today()
    hoje = int(datetime(day=agora.day,
                        month=agora.month,
                        year=agora.year).timestamp())
    return hoje

def agora():
    return int(datetime.today().timestamp())

#array of epochs has format = [[epoch1, value1], [epoch2, value2],...]
def get_interval_means(interval, array_of_epochs, epoch_beginning, epoch_ending):
    #exceptions handling
    if(len(array_of_epochs)<1):
      print ("Error: entry array is null")
      return [[]]

    # calculando o numero de intervalos
    delta_epoch = epoch_ending - epoch_beginning
    number_of_intervals = int(delta_epoch/interval)

    # guardando um dicionário onde a chave é um indice incremental e os valores são os intervalos possíveis
    interval_dict = {0 : [epoch_beginning, epoch_beginning + interval]}
    for i in range(number_of_intervals - 1):
        interval_dict[i+1] = [interval_dict[i][0] + interval, interval_dict[i][1] + interval]

    # para cada registro no array_of_epochs, checar a qual intervalo ele pertence e adicioná-lo ao dicionário final, separado por intervalo
    array_of_epochs_by_interval = {}
    for epoch_value in array_of_epochs:
        for i, interval in interval_dict.items():
            if (epoch_value[0] >= interval[0] and epoch_value[0] < interval[1]):
                if (i in array_of_epochs_by_interval):
                    array_of_epochs_by_interval[i] += [epoch_value[1]]
                else:
                    array_of_epochs_by_interval[i] = [epoch_value[1]]
                break;

    # para cada intervalo, calcular a média, mínimo e máximo
    result = []
    for i, data_values in array_of_epochs_by_interval.items():
        sum_interval  = sum(data_values)
        mean_interval = float(sum_interval)/len(data_values)
        max_interval  = max(data_values)
        min_interval  = min(data_values)
        label         = "{} - {}".format(datetime.fromtimestamp(interval_dict[i][0]).strftime("%d/%m/%y %H:%M"), datetime.fromtimestamp(interval_dict[i][1]).strftime("%d/%m/%y %H:%M"))
        result += [[label, mean_interval, min_interval, max_interval]]

    return result
