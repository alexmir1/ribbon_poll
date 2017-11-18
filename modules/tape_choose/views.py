import datetime
from flask import render_template, g, redirect, url_for, request
from flask_login import login_required
from app import db, app
from app.models import Mark, Color, CurrentRound, Round, Choices, ComparingColors, User
from . import tape_choose, forms
from .ColorInput import ColorInput
from modules.feedback.form import Feedback
from modules.feedback.send_feedback import send_feedback, feedback_available
from flask_mail import Message
import mail_config
from app import mail


def new_round_notification(grade):
    """
    Forms the message about new round
    """

    round = CurrentRound.query.filter_by(grade=grade).first().round

    for user in User.query.filter_by(grade=grade):
        msg = Message(subject='Начался новый раунд', recipients=[user.email], sender=mail_config.MAIL_USERNAME,
                      html=render_template('new_round_notification.html', username=user.name,
                                           ends_at=round.next[0].starts_at if len(round.next) == 1 else None))
        mail.send(msg)


@tape_choose.before_request
def update_current_round():
    """
    Updating (or creating) current round if needed; updating users' votes on this round.
    """
    grades = app.config['GRADES']
    for grade in grades:
        current_round = CurrentRound.query.filter_by(grade=grade).first()
        participants = []
        if current_round is not None and len(current_round.round.next) == 1 and \
                        current_round.round.next[0].starts_at is not None and \
                        datetime.datetime.utcnow() >= current_round.round.next[0].starts_at:
            # handle the case: next round should be started already
            for colors in ComparingColors.query.filter_by(round=current_round.round).all():
                if colors.second_color_id is not None:
                    first_cnt = 0
                    second_cnt = 0
                    for choice in Choices.query.filter_by(comparing_colors=colors).all():
                        if choice.selected == 0:
                            first_cnt += 1
                        else:
                            second_cnt += 1
                    if first_cnt >= second_cnt:
                        participants.append(colors.first_color_id)
                    if first_cnt <= second_cnt:
                        participants.append(colors.second_color_id)
                else:
                    participants.append(colors.first_color_id)
            current_round.round = current_round.round.next[0]

            new_round_notification(grade)

        elif current_round is None:
            # handle the case: the first round is not still started
            first_round = Round.query.filter_by(grade=grade, previous_id=None).first()
            if first_round is not None and (first_round.starts_at is None or
                                                    datetime.datetime.utcnow() >= first_round.starts_at):
                current_round = CurrentRound(grade=grade, round=first_round)
                db.session.add(current_round)
                participants += list(map(lambda x: x.id, Color.query.all()))

                new_round_notification(grade)

        # now, using collected list of participants, update CompairingColors pairs and Choices
        for i in range(1, len(participants), 2):
            colors = ComparingColors(first_color_id=participants[i - 1], second_color_id=participants[i],
                                     round=current_round.round)
            db.session.add(colors)
            for user in User.query.filter_by(grade=grade):
                mark1 = Mark.query.filter_by(user=user, color_id=colors.first_color_id).first()
                mark2 = Mark.query.filter_by(user=user, color_id=colors.second_color_id).first()
                if mark1 is not None and mark2 is not None and mark1.mark != mark2.mark:
                    db.session.add(Choices(comparing_colors=colors, selected=int(mark2.mark > mark1.mark), user=user))
        if len(participants) % 2 == 1:
            db.session.add(ComparingColors(first_color_id=participants[-1], round=current_round.round))
        db.session.commit()


@tape_choose.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    current_round = CurrentRound.query.filter_by(grade=g.user.grade).first()
    if current_round is not None:
        return redirect(url_for('tape_choose.vote_in_round', round_id=current_round.round_id))
    else:
        return "Нет доступных раундов"


@tape_choose.route('/vote/<int:round_id>', methods=['GET', 'POST'])
@login_required
def vote_in_round(round_id):
    if CurrentRound.query.filter_by(grade=g.user.grade).first() is None or \
                    CurrentRound.query.filter_by(grade=g.user.grade).first().round_id != round_id:
        return "Раунд недоступен"
    colors = []
    for comparing in ComparingColors.query.filter_by(round_id=round_id).all():
        if comparing.second_color_id is not None:
            colors.append(ColorInput(comparing))
    form = forms.gen_vote_form(colors)
    rf = Feedback()
    if form.validate_on_submit():
        send_feedback(rf, request.headers)
        for comparing in ComparingColors.query.filter_by(round_id=round_id).all():
            for choice in Choices.query.filter_by(user=g.user, comparing_colors=comparing).all():
                db.session.delete(choice)
        for color in colors:
            if color.input.data != 'None':
                db.session.add(Choices(user=g.user, comparing_colors_id=int(color.id), selected=int(color.input.data)))
        db.session.commit()
        return redirect(url_for('index'))
    else:
        if request.method == 'GET':
            for color in colors:
                choice = Choices.query.filter_by(user=g.user, comparing_colors_id=int(color.id)).first()
                if choice is not None:
                    color.input.data = str(choice.selected)
                    color.inputs[choice.selected].checked = True
        return render_template('vote.html', form=form, pairs=colors, rf=rf, feedback_available=feedback_available())


@tape_choose.route('/results')
def results():
    grades = app.config['GRADES']
    return render_template('results.html', grades=grades)


@tape_choose.route('/results/<grade>')
def result_in_grade(grade):
    grades = app.config['GRADES']
    rounds = Round.query.filter_by(grade=grade).all()
    ordered_rounds = [Round.query.filter_by(grade=grade, previous_id=None).first()]
    if ordered_rounds[0] is None:
        ordered_rounds = []
    else:
        while len(ordered_rounds[-1].next) == 1:
            ordered_rounds.append(ordered_rounds[-1].next[0])
    marks = dict()
    voters = dict()
    for round in rounds:
        marks[round.id] = dict()
        voters[round.id] = dict()
        for colors in round.colors:
            marks[round.id][colors.first_color_id] = 0
            marks[round.id][colors.second_color_id] = 0
            for choice in colors.choices:
                if choice.selected == 0:
                    marks[round.id][colors.first_color_id] += 1
                else:
                    marks[round.id][colors.second_color_id] += 1
                voters[round.id][choice.user.name] = voters[round.id].get(choice.user.name, 0) + 1
    return render_template('result_in_grade.html', grades=grades, marks=marks, voters=voters, rounds=ordered_rounds,
                           rounds_number=len(rounds), cur_grade=grade,
                           current_time=datetime.datetime.utcnow())
