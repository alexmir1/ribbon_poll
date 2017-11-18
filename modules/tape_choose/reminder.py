"""
    A script that reminds all users about the start of new round using email
    If executed with test parameter ('>> python reminder.py test'), reminder sends a message to developers only
"""

from app import app
from flask import render_template_string
from app.models import User, CurrentRound, Round
from app import mail
from flask_mail import Message
from modules.tape_choose.views import update_current_round
import mail_config
import config

import sys
import argparse


def form_message(grade):
    """
    Forms the message about new round
    """
    grade_round = CurrentRound.query.filter_by(grade=grade).first()
    if grade_round is None:
        return None

    cur_round = grade_round.round
    if cur_round is None:
        return None

    with app.app_context():
        with open('message.html') as f:
            return render_template_string(f.read(), round=cur_round)


def remind(grade):
    """
    Sends message about new round to every person
    """

    text = form_message(grade)
    if text is None:
        return
    msg = Message(text, sender=mail_config.MAIL_USERNAME, recipients=[user.email for user in User.query.filter_by(grade=grade).all()])
    mail.send(msg)


def test_remind():
    """
    Test version of 'remind()': sends the message to leha-kartoha and maksim-apelsin
    """
    text = form_message('b3')
    if text is None:
        return
    msg = Message(text, sender=mail_config.MAIL_USERNAME, recipients=[mail_config.MAIL_USERNAME, 's18b3_lavrik@179.ru'])
    mail.send(msg)


def main():
    for grade in config.GRADES:
        cur_round = CurrentRound.query.filter_by(grade=grade).first()
        update_current_round()
        new_round = CurrentRound.query.filter_by(grade=grade).first()

        if cur_round != new_round:
            parser = argparse.ArgumentParser()
            parser.add_argument('name', nargs='?')
            namespace = parser.parse_args(sys.argv[1:])

            if namespace.name == 'test':
                test_remind()
            else:
                remind(grade)

main()