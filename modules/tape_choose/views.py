from flask import render_template, g, redirect, url_for, request
from flask_login import login_required
from app import db
from app.models import Mark, Color
from . import tape_choose, forms
from .ColorInput import ColorInput


@tape_choose.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    colors = []
    for color in Color.query.all():
        colors.append(ColorInput(hex=color.hex, image=color.image_link, id=color.id))

    form = forms.gen_vote_form(colors)
    if form.validate_on_submit():
        for mark in Mark.query.filter_by(user=g.user).all():
            db.session.delete(mark)
        for color in colors:
            if color.input.data is not None:
                db.session.add(Mark(user_id=g.user.id, color_id=color.id, mark=color.input.data))
        return redirect(url_for('index'))
    else:
        if request.method == 'GET':
            for color in colors:
                mark = Mark.query.filter_by(user_id=g.user.id, color_id=color.id).first()
                if mark is not None:
                    color.input.data = mark.mark
        return render_template('vote.html', form=form, tapes=colors)

