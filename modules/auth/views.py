import httplib2
from oauth2client import client
from apiclient import discovery
from flask import render_template, g, redirect, url_for, request
from flask_login import login_user, logout_user
from app import db, lm
from . import auth
from .get_grade import get_grade
from app.models import User


@auth.route('/')
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'],
        redirect_uri=url_for('auth.login', _external=True))
    if 'code' in request.args:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        http_auth = credentials.authorize(httplib2.Http())
        oauth2 = discovery.build('oauth2', 'v2', http=http_auth)
        user_info = oauth2.userinfo().get().execute()
        email = user_info['email']
        grade = get_grade(email)
        if grade is None:
            print('wrong email: {}'.format(email))
            return render_template('wrong_email.html', email=email)
        else:
            user = User.query.filter_by(email=email).first()
            if user is None:
                name = user_info['name']
                user = User(email=email, grade=grade, name=name)
                db.session.add(user)
                db.session.commit()
            login_user(user)
            return render_template('success.html', email=email, grade=grade)
    else:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)


@auth.route('/logout')
def logout():
    if g.user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)