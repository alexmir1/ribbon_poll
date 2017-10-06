"""
    server and models configurations
"""

import os
from mail_config import *
BASEDIR = os.path.abspath(os.path.dirname(__file__))

host = 'localhost'
port = 8080
debug = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'DFBDFSFVfsbddf'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_migrate_repo')

MODULES = ['auth', 'tape_choose', 'feedback']

GRADES = ['b' + str(x) for x in range(1, 4)]

PREFERRED_URL_SCHEME = 'http' if os.environ.get('HEROKU') is None else 'https'

feedback_limit = 10