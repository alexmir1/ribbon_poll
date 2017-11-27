"""
    A script that reminds all users about the start of new round using email
"""
from datetime import timedelta, datetime
from flask import render_template
from app.models import User, CurrentRound, Choices, ComparingColors
from app.send_email import send_email
from app import app
from flask_mail import Message
from modules.tape_choose.views import update_current_round
import mail_config
import config


def remind(grade):
    """
    Forms the message about new round
    """
    grade_round = CurrentRound.query.filter_by(grade=grade).first()
    if grade_round is None:
        return
    round = grade_round.round

    for user in User.query.filter_by(grade=grade):
        has_participated = False
        for colors in ComparingColors.query.filter_by(round=round):
            has_participated = has_participated or \
                               Choices.query.filter_by(comparing_colors=colors, user=user).first() is not None
        if not has_participated:
            msg = Message(subject='Конец раунда близко', recipients=[user.email], sender=mail_config.MAIL_USERNAME,
                          html=render_template('end_round_notification.html', username=user.name,
                                               ends_at=round.next[0].starts_at))
            send_email(msg)


if __name__ == '__main__':
    with app.app_context():
        update_current_round()
        for grade in config.GRADES:
            grade_round = CurrentRound.query.filter_by(grade=grade).first()
            if grade_round is not None:
                round = grade_round.round
                if len(round.next) == 1 and round.next[0].starts_at is not None:
                    for delta in config.REMIND_HOURS:
                        if abs(datetime.utcnow() + timedelta(hours=delta) - round.next[0].starts_at) <\
                                timedelta(minutes=30):
                            remind(grade)
