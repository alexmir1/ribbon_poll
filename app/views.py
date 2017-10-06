from app import app, db
from flask import render_template, g, redirect, url_for
from flask_login import login_required, current_user


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(500)
def e500(error):
    print(error)
    return render_template('500.html')
