from app import app, db
from flask import render_template, g, redirect, url_for
from flask_login import login_required, current_user


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def index():
    return render_template('index.html')
