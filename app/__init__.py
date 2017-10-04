"""
app initialization
"""
import importlib
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager



db = SQLAlchemy()
migrate = Migrate()

lm = LoginManager()


def create_app():
    """
    create and init Flask app and it's models
    :return: Flask app
    """
    app = Flask(__name__)
    app.config.from_object('config')

    migrate.init_app(app, db)

    lm.init_app(app)
    lm.login_view = 'auth.login'

    db.init_app(app)

    for module in app.config['MODULES']:
        module_name = importlib.import_module('modules.' + module)

        module_blueprint = getattr(module_name, module)

        app.register_blueprint(module_blueprint, url_prefix='/' + module)

    return app


app = create_app()

from app import views, models