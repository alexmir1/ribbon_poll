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

    print('[-]USER Warning: deprecation resolve: SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config.update({'SQLALCHEMY_TRACK_MODIFICATIONS': True})

    migrate.init_app(app, db)

    lm.init_app(app)

    db.init_app(app)

    return app


app = create_app()
from app import views, models
