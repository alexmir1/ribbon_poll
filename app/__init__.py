"""
app initialization
"""
import importlib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager(app)
lm.login_view = 'auth.login'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

mail = Mail(app)

for module in app.config['MODULES']:
    module_name = importlib.import_module('modules.' + module)

    module_blueprint = getattr(module_name, module)

    app.register_blueprint(module_blueprint, url_prefix='/' + module)


from app import views, models