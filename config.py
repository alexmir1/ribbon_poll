"""
    server and models configurations
"""

import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

host = '0.0.0.0'
port = 8080
debug = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'THRG8r965ff5'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_migrate_repo')

MODULES = ['auth']
