# -*- coding: utf-8 -*-
"""
Created on Wed May 17 00:20:42 2017

@author: Brian Confessor e Débora Pina
"""

from ..common.mail import send_email
from ..models import  AdministradorSistema
import os.path
from . import db

def get_lab_name(lab_id):
    data = db.fetchone("""SELECT nome FROM Lab WHERE lab_id = ?;""", (lab_id,))
    lab_name = data[0]
    return lab_name

#returns -1 if lights are; x > 0 otherwise, x = number of (last person present + admins who will receive emails)
def check_for_forgotten_lights(lab_id):
    data = db.fetchall("""SELECT User_Lab.email FROM User_Lab, Presenca WHERE User_Lab.user_id = Presenca.user_id AND Presenca.presente=1 AND Presenca.lab_id = ?;""", (lab_id,))
    present_users =[]
    for row in data:
        present_users.append(str(row[0]))

    if(len(present_users)==0):
        data = db.fetchone("""SELECT lum
                              FROM Log_Lab WHERE lab_id = ? ORDER BY data DESC;""", (lab_id,))
        lights_on = (data[0] == 1)

        if(lights_on):
            lab_name = get_lab_name(lab_id)
            subject = "Aviso de luz acesa"
            msg_content = """
Caro responsável,
Você está recebendo essa mensagem pois a luz do laboratorio """ + lab_name + """ foi deixada acesa e não há mais funcionários presentes.
Pedimos que procure uma solução quanto a isso, para evitar o gasto desnecessário de energia.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

            admins = AdministradorSistema.obter_administradores()
            emails = [a.email for a in admins]
            data = db.fetchone("""SELECT u.email
                                  FROM Log_Presenca l, User_Lab u WHERE l.lab_id=? AND l.evento='OUT' AND l.user_id = u.user_id ORDER BY l.data DESC;""", (lab_id,))
            emails += [data[0]]
            send_email(subject, msg_content, emails)
            return len(emails)

        #lights were off
        else:
            return -1
    else:
        return "presentes"


#returns -1 if temperature is ok; x > 0 otherwise, x = number of present people + admins who will receive emails
def check_for_abnormal_temperature(lab_id):
    data = db.fetchone("""
        SELECT temp_min, temp_max
        FROM Zona_de_Conforto_Lab z, Lab l
        WHERE z.zona_conforto_id = l.zona_conforto_id AND lab_id = ?""", (lab_id,))

    temp_min=data[0]
    temp_max=data[1]
    

    data = db.fetchone("""
        SELECT temp
        FROM Log_Lab WHERE lab_id = ? ORDER BY data DESC; """, (lab_id,))

    current_temp = data[0]

    if (current_temp < temp_min or current_temp > temp_max):
        lab_name = get_lab_name(lab_id)
        subject = "Aviso de temperatura anormal"
        msg_content = """
Caro responsável,
Você está recebendo essa mensagem pois a temperatura do laboratorio """ + lab_name + """ se encontra fora da zona de conforto.
Pedimos que procure uma solução quanto a isso.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

        admins = AdministradorSistema.obter_administradores()
        emails = [a.email for a in admins]

        data = db.fetchall("""
            SELECT u.email
            FROM Presenca p
            INNER JOIN User_Lab u
              ON p.user_id = u.user_id
            WHERE presente = 1 AND lab_id = ?; """, (lab_id,))

        if len(data) != 0:
            for d in data:
                emails += [d[0]]

        send_email(subject, msg_content, emails)
        return len(emails)

    #normal temperature
    else: 
        return -1



#returns -1 if temperature is ok; x > 0 otherwise, x = number of present people + admins who will receive emails
def check_for_abnormal_humidity(lab_id):
    data = db.fetchone("""
        SELECT umid_min, umid_max
        FROM Zona_de_Conforto_Lab z, Lab l
        WHERE z.zona_conforto_id = l.zona_conforto_id AND lab_id = ?""", (lab_id,))


    umid_min=data[0]
    umid_max=data[1]

    data = db.fetchone("""
        SELECT umid
        FROM Log_Lab WHERE lab_id = ? ORDER BY data DESC; """, (lab_id,))

    current_umid = data[0]

    if (current_umid < umid_min or current_umid > umid_max):
        lab_name = get_lab_name(lab_id)
        subject = "Aviso de umidade anormal"
        msg_content = """
Caro responsável,
Você está recebendo essa mensagem pois a umidade do laboratorio """ + lab_name + """  se encontra fora da zona de conforto.
Pedimos que procure uma solução quanto a isso.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

        admins = AdministradorSistema.obter_administradores()
        emails = [a.email for a in admins]

        data = db.fetchall("""
            SELECT u.email
            FROM Presenca p
            INNER JOIN User_Lab u
              ON p.user_id = u.user_id
            WHERE presente = 1 AND lab_id = ?; """, (lab_id,))

        if len(data) != 0:
            for d in data:
                emails += [d[0]]

        send_email(subject, msg_content, emails)
        return len(emails)

    #normal humidity
    else:
        return -1


def check_for_equipment_temperature(equipment_id, lab_id):
    data = db.fetchone("""
    SELECT temp_min, temp, temp_max
    FROM Log_Equip
    INNER JOIN Equip ON Log_Equip.equip_id = Equip.equip_id
    WHERE Equip.equip_id = ?
    ORDER BY data DESC""", (equipment_id,))

    if (data == None):
        return "Data is none"

    if (data[1] < data[0] or data[1] > data[2]):
        lab_name = get_lab_name(lab_id)
        subject = "Aviso de temperatura anormal no equipamento"
        msg_content = """
Caro responsável,
Você está recebendo essa mensagem pois a temperatura do equipamento """ + str(equipment_id) + """ do laboratorio """ + lab_name + """ se encontra fora da zona de conforto.
Pedimos que procure uma solução quanto a isso.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

        admins = AdministradorSistema.obter_administradores()
        emails = [a.email for a in admins]

        data = db.fetchall("""
            SELECT u.email
            FROM Presenca p
            INNER JOIN User_Lab u
              ON p.user_id = u.user_id
            WHERE presente = 1 AND lab_id = ?; """, (lab_id,))

        if len(data) != 0:
            for d in data:
                emails += [d[0]]

        send_email(subject, msg_content, emails)
        return 1
    else:
        return -1
