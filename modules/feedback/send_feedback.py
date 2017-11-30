from flask import render_template_string, g, request
from flask_mail import Message
from app import app
from app.send_email import send_email


def feedback_available():
    return g.user.feedback_count < app.config['FEEDBACK_LIMIT']


def send_feedback(form, headers):
    if feedback_available() and (form.usability.data.strip() != '' or
                                 form.usefulness.data.strip() != '' or
                                 form.designing.data.strip() != '' or
                                 form.comment.data.strip() != ''):
        msg = Message('{} - tape-choose feedback'.format(g.user.name),
                      recipients=app.config['ADMINS'], reply_to=g.user.email,
                      html=render_template_string(open('modules/feedback/templates/feedback_mail.html').read(),
                                                  name=g.user.name, grade=g.user.grade,
                                                  usability=form.usability.data, usefulness=form.usefulness.data,
                                                  designing=form.designing.data, comment=form.comment.data,
                                                  headers=str(headers), version=request.form.get('version')))
        send_email(msg)
        g.user.feedback_count += 1
