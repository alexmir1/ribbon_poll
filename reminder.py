"""
    A script that reminds all users about the start of new round using email
    If executed with test parameter ('>> python reminder.py test'), reminder sends a message to developers only
"""

from app.models import User, CurrentRound, Round
from app import mail
from flask_mail import Message
import mail_config

import sys
import argparse


def form_message():
    """
    Forms the message about new round
    """
    res = ''
    res += 'Добрый день!\n\n'
    res += 'Напоминаем, что {} начнется {} раунд голосования за цвет ленты. Не упустите шанс ' \
           'помочь любимому цвету дойти до пьедестала почета! Соревнование проходит по олимпийской системе.\n\n'
    res += 'http://s18-179.herokuapp.com/'
    cur_round = Round.query.filter_by(id=CurrentRound.round_id).first()

    if cur_round is None:
        return None
    else:
        return res.format(cur_round.starts_at, cur_round.id)


def remind():
    """
    Sends message about new round to every person
    """
    text = form_message()
    if text is None:
        return
    msg = Message(text, sender=mail_config.MAIL_USERNAME, recipients=[user.email for user in User.query.all()])
    mail.send(msg)


def test_remind():
    """
    Test version of 'remind()': sends the message to leha-kartoha and maksim-apelsin
    """
    text = form_message()
    if text is None:
        return
    msg = Message(text, sender=mail_config.MAIL_USERNAME, recipients=[mail_config.MAIL_USERNAME, 's18b3_lavrik@179.ru'])
    mail.send(msg)


parser = argparse.ArgumentParser()
parser.add_argument('name', nargs='?')
namespace = parser.parse_args(sys.argv[1:])


if namespace.name == 'test':
    test_remind()
else:
    remind()