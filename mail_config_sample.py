import os
if os.environ.get('DATABASE_URL') is None:
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 's18b3_mironov@179.ru'
    MAIL_PASSWORD = '***'
else:
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_USERNAME = os.environ.get('SENDGRID_USERNAME')
    MAIL_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
# administrator list
ADMINS = ['s18b3_mironov@179.ru']
