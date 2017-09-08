"""
    server and models configurations
"""

import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

host = '0.0.0.0'
port = 5000
debug = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'THRG8r965ff5'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_migrate_repo')
