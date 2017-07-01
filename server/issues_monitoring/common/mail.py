"""
Created on Sat Apr 29 14:48:16 2017

@author: BRC
"""

from .. import Config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import smtplib

def send_email(subject, message, emails):
    # Writing the message
    _from = "Sistema ISSUES Monitoring <{}>".format(Config.email)

    msg = MIMEMultipart()
    msg['From'] = _from
    msg['To'] = COMMASPACE.join(emails)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, "plain", "utf-8"))

    # Sending the mail
    try:
        # print("Starting SMTP server...")
        server = smtplib.SMTP(Config.smtp_host.host, Config.smtp_host.port)
        server.ehlo()
        server.starttls()
        server.ehlo()

        # print("Logging in...")
        server.login(Config.email, Config.email_password)
        # print("Sending emails...")
        server.sendmail("", emails, msg.as_string())
        server.quit()
        # print("Emails sent!")
    except Exception as e:
        print("Error: Couldn't open the mail server.\n", repr(e))
