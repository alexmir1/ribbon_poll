import smtplib
from time import sleep
from app import mail, app
from app.decorators import async


@async
def send_email(msg):
    with app.app_context():
        cnt = 0
        while True:
            try:
                mail.send(msg)
            except smtplib.SMTPServerDisconnected:
                cnt += 1
                if cnt == 30:
                    print('finally cant send an email to {}'.format(msg.recipients[0]))
                    break
                print('cant send an email')
                sleep(2)
            else:
                break
