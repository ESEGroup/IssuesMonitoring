# -*- coding: utf-8 -*-
"""
Created on Mon May  1 01:01:57 2017

@author: BRC
"""
import sqlite3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib

#Sends email to person responsible for the lab, letting them know a new user awaits approval
#to be registered to the Database

def SendNewUserNotification(username, password):
    
    # Writing the message    
    fro = "Sistema ISSUES Monitoring <cos603.issuesmonitoring@gmail.com>"
    msgContent = """
Caro responsável,
Você está recebendo essa mensagem pois um novo usuário foi cadastrado no banco de dados do sistema ISSUES Monitoring.
Para continuar o processo de cadastro do novo usuário, por favor entre no site do sistema com seu nome de usuário e senha e aprove o cadastro.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

    conn = sqlite3.connect("Issues.db")
    supervisorEmail = ""
    #recebe ID de users que estam presentes
    try:
        cursor = conn.execute("SELECT email from User_Sys, where admin=1")
        for row in cursor:
            supervisorEmail = row[0]
    except sqlite3.OperationalError:
        print("ERROR: Could not find Database")
    
    msg = MIMEMultipart()
    msg['From']=fro
    msg['To']=supervisorEmail
    msg['Date']=formatdate(localtime=True)
    msg['Subject']="Alerta de cadastro de novo usuário"
    msg.attach(MIMEText(msgContent, "plain", "utf-8"))

    # Gmail login credentials
    USERNAME = username
    PASSWORD = password
    
    # Sending the mail  
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        
        server.login(USERNAME,PASSWORD)
        server.sendmail("", supervisorEmail, msg.as_string())
        server.quit()
    except:
        print ("Error: Couldn't open the mail server.")

