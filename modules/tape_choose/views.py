from flask import render_template, g, redirect, url_for, request
from flask_login import login_required
from app import db, app
from app.models import Mark, Color, User
from . import tape_choose, forms
from .ColorInput import ColorInput
from modules.feedback.form import Feedback
from modules.feedback.send_feedback import send_feedback, feedback_available


@tape_choose.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    colors = []
    for color in Color.query.all():
        colors.append(ColorInput(hex=color.hex, image=color.image_link, id=color.id))

    form = forms.gen_vote_form(colors)
    rf = Feedback()
    if form.validate_on_submit():
        send_feedback(rf, request.headers)
        for mark in Mark.query.filter_by(user=g.user).all():
            db.session.delete(mark)
        for color in colors:
            if color.input.data is not None:
                db.session.add(Mark(user_id=g.user.id, color_id=color.id, mark=color.input.data))
        db.session.commit()
        return redirect(url_for('index'))
    else:
        if request.method == 'GET':
            for color in colors:
                mark = Mark.query.filter_by(user_id=g.user.id, color_id=color.id).first()
                if mark is not None:
                    color.input.data = mark.mark
        return render_template('vote.html', form=form, tapes=colors, rf=rf, feedback_available=feedback_available())


@tape_choose.route('/results')
def results():
    colors = Color.query.all()
    grades = app.config['GRADES']
    marks = dict([(color.id, dict([(grade, [0, 0]) for grade in grades])) for color in colors])
    db_marks = Mark.query.all()
    voters = dict([(grade, dict()) for grade in grades])
    for mark in db_marks:
        try:
            marks[mark.color_id][mark.user.grade][0] += mark.mark
            marks[mark.color_id][mark.user.grade][1] += 1
            voters[mark.user.grade][mark.user.name] = voters[mark.user.grade].get(mark.user.name, 0) + 1
        except KeyError as error:
            print(error)
    for x in marks.values():
        for y in x.values():
            if y[1] > 0:
                y[0] /= y[1]
            else:
                y[0] = None
    return render_template('results.html', colors=colors, grades=grades, marks=marks, voters=voters)
