from ..models import (Laboratorio, Evento, UsuarioLab, Computador,
                      ZonaConforto, Anomalia, AdministradorSistema,
                      Sistema)
from threading import Thread
from datetime import datetime
from ..common.mail import send_email
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

def cadastro_equipamento(lab_id, nome, descricao, temp_min, temp_max, MAC, parent_id):
    equipamento = Computador(lab_id, nome, descricao, temp_min, temp_max, MAC, parent_id)
    equipamento.cadastrar()

def remover_equipamento(_id):
    Computador.remover(_id)

def obter_ids_equipamentos(id):
    return Laboratorio.obter_todos_ids_equipamentos(id)

def obter_nome_equipamentos(id):
    return Laboratorio.obter_nome_equipamentos(id)

def obter_zona_de_conforto(id):
    return ZonaConforto.obter(id)

def obter_laboratorios_id():
    return Laboratorio.obter_todos_ids()

def checar_temperatura(lab_id, lab_nome, temperatura, zona_conforto, emails, data):
    if temperatura < zona_conforto.temp_min or temperatura > zona_conforto.temp_max:
        subject = "Aviso de temperatura anormal"
        msg_content = """
Caro responsável,
Você está recebendo essa mensagem pois a temperatura do laboratorio """ + lab_nome + """ se encontra fora da zona de conforto.
Pedimos que procure uma solução quanto a isso.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

        if temperatura < zona_conforto.temp_min:
            slug = "temp-min"
            anti_slug = "temp-max"
            temp_limite = zona_conforto.temp_min
        else:
            slug = "temp-max"
            anti_slug = "temp-min"
            temp_limite = zona_conforto.temp_max

        id, nao_repetida = Anomalia.nao_repetida(slug, anti_slug)
        if nao_repetida:
            Anomalia.registrar_anomalia(lab_id, slug, int(temperatura), temp_limite)
            send_email(subject, msg_content, emails)
        else:
            Anomalia.atualizar_valor(id, int(temperatura), data)

def checar_umidade(lab_id, lab_nome, umidade, zona_conforto, emails, data):
    if umidade < zona_conforto.umidade_min or umidade > zona_conforto.umidade_max:
        subject = "Aviso de umidade anormal"
        msg_content = """
Caro responsável,
Você está recebendo essa mensagem pois a umidade do laboratorio """ + lab_nome + """  se encontra fora da zona de conforto.
Pedimos que procure uma solução quanto a isso.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

        if umidade < zona_conforto.umidade_min:
            slug = "umid-min"
            anti_slug = "umid-max"
            umid_limite = zona_conforto.umidade_min
        else:
            slug = "umid-max"
            anti_slug = "umid-min"
            umid_limite = zona_conforto.umidade_max

        id, nao_repetida = Anomalia.nao_repetida(slug, anti_slug)
        if nao_repetida:
            Anomalia.registrar_anomalia(lab_id, slug, int(umidade), umid_limite)
            send_email(subject, msg_content, emails)
        else:
            Anomalia.atualizar_valor(id, int(umidade), data)

def checar_luz_acesa_vazio(lab_id, lab_nome, luminosidade, emails, data):
    if luminosidade == 1:
        subject = "Aviso de luz acesa"
        msg_content = """
Caro responsável,
Você está recebendo essa mensagem pois a luz do laboratorio """ + lab_nome + """ foi deixada acesa e não há mais pessoas presentes.
Pedimos que procure uma solução quanto a isso, para evitar o gasto desnecessário de energia.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

        slug = "luz"
        if not Anomalia.nao_repetida(slug):
            emails += Laboratorio.email_ultimo_a_sair(lab_id)
            Anomalia.registrar_anomalia(lab_id, slug)
            send_email(subject, msg_content, emails)
        else:
            Anomalia.atualizar_valor(id, None, data)

def checar_temperatura_equipamento(lab_id, lab_nome, equip_id, emails,
                                   data_inicio, data_final, data):
    (temp_min,
     temperatura,
     temp_max,
     equip_nome) = Computador.obter_medida(equip_id,
                                           data_inicio,
                                           data_final)

    if temperatura < temp_min or temperatura > temp_max:
        subject = "Aviso de temperatura anormal no equipamento"
        msg_content = """
Caro responsável,
Você está recebendo essa mensagem pois a temperatura do equipamento """ + equip_nome + """ do laboratorio """ + lab_nome + """ se encontra fora da zona de conforto.
Pedimos que procure uma solução quanto a isso.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

        if temperatura < temp_min:
            slug = "temp-equip-min"
            anti_slug = "temp-equip-max"
            temp_limite = temp_min
        else:
            slug = "temp-equip-max"
            anti_slug = "temp-equip-min"
            temp_limite = temp_max

        id, nao_repetida = Anomalia.nao_repetida(slug, anti_slug)
        if nao_repetida:
            Anomalia.registrar_anomalia(lab_id,
                                        slug,
                                        int(temperatura),
                                        temp_limite,
                                        equip_id)
            send_email(subject, msg_content, emails)
        else:
            Anomalia.atualizar_valor(id, int(temperatura), data)

def checar_condicoes_ambiente(lab_id):
    data_inicio = Sistema.obter_data_inicio()
    while (True):
        nome = Laboratorio.nome(lab_id)
        admins = AdministradorSistema.obter_administradores()
        equips = obter_ids_equipamentos(lab_id)

        emails = [a.email for a in admins]
        presentes = Laboratorio.presentes(lab_id)
        emails += presentes

        zona_de_conforto = ZonaConforto.obter(lab_id)

        data_final = int(datetime.now().timestamp())

        data, temperatura, umidade, lum = Laboratorio.obter_ultima_medida(lab_id, data_inicio, data_final)
        if zona_de_conforto is not None and data is not None:
            if len(presentes) == 0:
                checar_luz_acesa_vazio(lab_id, nome, lum, emails, data)

            if len(emails) > 0 and None not in [temperatura, umidade]:
                checar_temperatura(lab_id, nome, temperatura, zona_de_conforto, emails, data)
                checar_umidade(lab_id, nome, umidade, zona_de_conforto, emails, data)

                for eq in equips:
                    checar_temperatura_equipamento(lab_id, nome, eq, emails, data_inicio, data_final, data)

        Sistema.definir_data_inicio(data_final)
        check_intervalo = 1. #TODO: Pegar do Banco de Dados
        check_intervalo_sec = check_intervalo*60.
        sleep(check_intervalo_sec)

def get_data_log(chart_type, chart_target, start_date, end_date, lab_id):
    if chart_type == "temperatura":
        if chart_target == "laboratorio":
            data = Laboratorio.obter_temperatura_entre_tempos_lab(start_date, end_date, lab_id)
            return data
        else:
            equip_id = chart_target
            data = Computador.obter_medidas_entre_tempos_equip(start_date, end_date, equip_id)
            return data
    elif chart_type == "umidade":
        data = Laboratorio.obter_umidade_entre_tempos_lab(start_date, end_date, lab_id)
        return data

def obter_anomalias(lab_id):
    return Laboratorio.obter_anomalias(lab_id)

def obter_intervalo_arduino(lab_id):
    return Laboratorio.obter_intervalo_arduino(lab_id)

def obter_equipamentos(lab_id):
    return Computador.obter_do_lab(lab_id)

def atualizar_equipamento(lab_id, nome_equip, descricao, temp_min, temp_max, MAC, parent_id, id):
    equip = Computador(lab_id, nome_equip, descricao, temp_min, temp_max, MAC, parent_id, id=id)
    equip.editar()

def obter_equipamento(id):
    return Computador.obter(id)

def obter_dados_entre_tempos(tempo_inicio, tempo_final, lab_id):
    return Laboratorio.obter_dados_entre_tempos_lab(tempo_inicio, tempo_final, lab_id)

def obter_dados_entre_tempos_equip(tempo_inicio, tempo_final, lab_id):
    return Computador.obter_medidas_entre_tempos_equip(tempo_inicio, tempo_final, lab_id)
