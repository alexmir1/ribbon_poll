from flask import render_template_string, g
from flask_mail import Message
from app import app, mail


def feedback_available():
    return g.user.feedback_count < app.config['feedback_limit']


def send_feedback(form, headers):
    if feedback_available() and (form.usability.data.strip() != '' or
                                                                 form.usefulness.data.strip() != '' or
                                                                 form.designing.data.strip() != '' or
                                                                 form.comment.data.strip() != ''):
        msg = Message('{} - tape-choose feedback'.format(g.user.name),
                      sender=app.config['ADMINS'][0], recipients=app.config['ADMINS'], reply_to=g.user.email,
                      html=render_template_string(open('modules/feedback/templates/feedback_mail.html').read(),
                                                  name=g.user.name, grade=g.user.grade,
                                                  usability=form.usability.data, usefulness=form.usefulness.data,
                                                  designing=form.designing.data, comment=form.comment.data,
                                                  headers=str(headers)))
        mail.send(msg)
        g.user.feedback_count += 1
