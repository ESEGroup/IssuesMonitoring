# -*- coding: utf-8 -*-
"""
Created on Wed May 17 00:20:42 2017

@author: Brian Confessor e Débora Pina
"""

from ..common.mail import send_email
from ..models import  AdministradorSistema
from . import db

#checks if lights were left on while no one was in lab
def CheckForForgottenLights():
    #checks for people in lab
    data = db.fetchall("""SELECT User_Lab.email 
                          FROM User_Lab, Presenca WHERE User_Lab.user_id=Presenca.user_id AND Presenca.presente=1;""")
    presentUsers =[]
    for row in data:
        presentUsers.append(str(row[0]))
    
    if(len(presentUsers)==0):
        #no one is in the lab, checks if lights are on
        data = db.fetchall("""SELECT lum 
                              FROM Log_Lab ORDER BY data DESC LIMIT 1;""")
        lightsOn=False
        for row in data:
            lightsOn=row[0]
            
        if(lightsOn):
            #lights are on, send email to supervisor
            subject = "Aviso de luz acesa"
            msgContent = """
Caro responsável,
Você está recebendo essa mensagem pois a luz do laboratorio foi deixada acesa e não há mais funcionários presentes.
Pedimos que procure uma solução quanto a isso, para evitar o gasto desnecessário de energia.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""
    
            admins = AdministradorSistema.obter_administradores()
            emails = [a.email for a in admins]
            #if it got here, just send message to supervisor(s)
            send_email(subject, msgContent, emails)