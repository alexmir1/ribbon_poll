import smtplib
from time import sleep
from app import mail, app
from app.decorators import async


@async
def send_email(msg):
    with app.app_context():
        while True:
            try:
                mail.send(msg)
            except smtplib.SMTPServerDisconnected:
                print('cant send an email')
                sleep(2)
            else:
                break
