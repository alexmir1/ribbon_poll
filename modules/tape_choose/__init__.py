"""
tape choose module init
"""

from flask import Blueprint

tape_choose = Blueprint('tape_choose', __name__, template_folder='templates', static_folder='static')

from . import views
