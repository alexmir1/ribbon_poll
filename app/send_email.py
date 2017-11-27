import smtplib
from time import sleep
from app import mail
from app.decorators import async


@async
def send_email(msg):
    while True:
        try:
            mail.send(msg)
        except smtplib.SMTPServerDisconnected:
            sleep(1)
        else:
            break
