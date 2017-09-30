from app import app, forms, db
from flask import render_template, g, redirect, url_for
from flask_login import login_required, current_user


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@login_required
def index():
    return g.user.email + ', grade: ' + g.user.grade

