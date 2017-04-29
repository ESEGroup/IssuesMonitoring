# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 14:48:16 2017

@author: BRC
"""
import sqlite3

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import smtplib



#users_list: list of users who will receive emails, taken from the DB(unused for now)
def SendEmailsToUsers(users_list):
    
    # Writing the message    
    fro = "Sistema ISSUES Monitoring <cos603.issuesmonitoring@gmail.com>"
    msgContent = """
Caro usuário,
Você está recebendo essa mensagem pois se encontra marcado como 'presente' no laboratório.
Informamos que às 00:00h de hoje, todos os logs de presença foram reiniciados.
Caso ainda se encontre no laboratório, pedimos que renove seu registro de presença.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

    msg = MIMEMultipart()
    msg['From']=fro
    msg['To']=COMMASPACE.join(users_list)
    msg['Date']=formatdate(localtime=True)
    msg['Subject']="Alerta de Reset de presenças"
    msg.attach(MIMEText(msgContent, "plain", "utf-8"))

    # Gmail login credentials
    USERNAME = 'cos603.issuesmonitoring@gmail.com'
    PASSWORD = 'COS603_2017'
    
    # Sending the mail  
    try:
        #print("Starting SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        
        #print("Logging in...")
        server.login(USERNAME,PASSWORD)
        #print ("Sending emails...")
        server.sendmail("", users_list, msg.as_string())
        server.quit()
        #print ("Emails sent!")
    except:
        print ("Error: Couldn't open the mail server.")


def ResetRegisteredUsers():
    conn = sqlite3.connect("Issues.db")
    
    #recebe ID de users que estam presentes
    try:
        cursor = conn.execute("SELECT User_Lab.email from User_Lab, Presenca where User_Lab.user_id=Presenca.user_id AND Presenca.presente=1")
        presentUsers =[]
        for row in cursor:
            presentUsers.append(str(row[0]))
            
        #Sending emails...
        SendEmailsToUsers(presentUsers)
        
        #apos enviar os emails necessarios, resetar presencas
        conn.execute("UPDATE Presenca set presente = 0")#Resets all presences
        conn.commit()
        conn.close()
        
    except sqlite3.OperationalError:
        print("ERROR: Could not find Database")
      
    