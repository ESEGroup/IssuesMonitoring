# -*- coding: utf-8 -*-
"""
Created on Wed May 17 00:20:42 2017

@author: Brian Confessor e Débora Pina
"""

from ..common.mail import send_email
from ..models import  AdministradorSistema
from . import db


def getLabName(lab_id):
    data = db.fetchone("""SELECT nome FROM Lab WHERE lab_id = ?;""", (lab_id,))
    lab_name = data[0]
    return lab_name

def CheckForForgottenLights(lab_id):
    data = db.fetchall("""SELECT User_Lab.email 
                          FROM User_Lab, Presenca WHERE User_Lab.user_id = Presenca.user_id AND Presenca.presente=1 AND Presenca.lab_id = ?;""", (lab_id,))
    presentUsers =[]
    for row in data:
        presentUsers.append(str(row[0]))
    
    if(len(presentUsers)==0):
        data = db.fetchall("""SELECT lum 
                              FROM Log_Lab WHERE lab_id = ? ORDER BY data DESC LIMIT 1;""", (lab_id,))
        lightsOn=False
        lightsOn = data[0]
            
        if(lightsOn):
            lab_name = getLabName(lab_id)
            subject = "Aviso de luz acesa"
            msgContent = """
Caro responsável,
Você está recebendo essa mensagem pois a luz do laboratorio """ + lab_name + """ foi deixada acesa e não há mais funcionários presentes.
Pedimos que procure uma solução quanto a isso, para evitar o gasto desnecessário de energia.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

            admins = AdministradorSistema.obter_administradores()
            emails = [a.email for a in admins]

            data = db.fetchall("""SELECT u.email
                                  FROM Log_Presenca l, User_Lab u WHERE l.lab_id=? AND l.evento='OUT' AND l.user_id = u.user_id ORDER BY l.data DESC LIMIT 1;""", (lab_id,))
            if(len(data) != 0):
                for d in data:
                    emails += [d[0]]           

            send_email(subject, msgContent, emails)

def CheckForEnvironmentConditions(lab_id):
    data = db.fetchall("""
        SELECT temp_min, temp_max, umid_min, umid_max 
        FROM Zona_de_Conforto_Lab z, Lab l 
        WHERE z.zona_conforto_id = l.zona_conforto_id AND lab_id = ?""", (lab_id,))

    umid_min=0
    umid_max=0
    temp_min=0
    temp_max=0

    for row in data:
        temp_min=row[0]
        temp_max=row[1]
        umid_min=row[2]
        umid_max=row[3]

    current_temp = 0
    current_umid = 0
    data = db.fetchall("""SELECT temp, umid 
                          FROM Log_Lab WHERE lab_id = ? ORDER BY data DESC LIMIT 1; """, (lab_id,))
    
    for row in data:
        current_temp = row[0]
        current_umid = row[1]
    
    if (current_temp < temp_min or current_temp > temp_max):
        lab_name = getLabName(lab_id)
        subject = "Aviso de temperatura anormal"
        msgContent = """
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

        send_email(subject, msgContent, emails)
        
    if (current_umid < umid_min or current_umid > umid_max):
        lab_name = getLabName(lab_id)
        subject = "Aviso de umidade anormal"
        msgContent = """
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

        send_email(subject, msgContent, emails)     

def checkForEquipmentTemperature(equipment_id, lab_id):
    print ("checking condicoes")
    data = db.fetchone("""
    SELECT temp_min, temp, temp_max
    FROM Log_Equip 
    INNER JOIN Equip ON Log_Equip.equip_id = Equip.equip_id 
    WHERE Equip.equip_id = ? 
    ORDER BY data DESC LIMIT 1""", (equipment_id,))
    
    if (data[1] < data[0] or data[1] > data[2]):
        lab_name = getLabName(lab_id)
        subject = "Aviso de temperatura anormal no equipamento"
        msgContent = """
Caro responsável,
Você está recebendo essa mensagem pois a temperatura do equipamento """ + str(equipment_id) + """ do laboratorio """ + lab_name + """ se encontra fora da zona de conforto.
Pedimos que procure uma solução quanto a isso.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

        admins = AdministradorSistema.obter_administradores()
        emails = [a.email for a in admins]
        print (emails)

        data = db.fetchall("""
            SELECT u.email
            FROM Presenca p
            INNER JOIN User_Lab u
              ON p.user_id = u.user_id
            WHERE presente = 1 AND lab_id = ?; """, (lab_id,))

        if len(data) != 0:
            for d in data:
                emails += [d[0]]   
        print (emails) 

        send_email(subject, msgContent, emails)