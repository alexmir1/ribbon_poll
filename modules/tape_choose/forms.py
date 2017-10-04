from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import NumberRange, Optional


def gen_vote_form(colors):
    form_vals = dict()
    for color in colors:
        form_vals.update([('c' + color.hex, IntegerField('c' + color.hex,
                                                         validators=[Optional(), NumberRange(1, 100)]))])
    form = type('VoteForm', (FlaskForm,), form_vals)()
    for color in colors:
        color.input = form.__getattribute__('c' + color.hex)
    return form
