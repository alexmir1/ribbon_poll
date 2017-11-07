from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.validators import Optional


def gen_vote_form(colors):
    form_vals = dict()
    for color in colors:
        form_vals['c' + color.id] = RadioField('c' + color.id, choices=[('0', '0'), ('1', '1')], validators=[Optional()])
    form = type('VoteForm', (FlaskForm,), form_vals)()
    for color in colors:
        color.input = form.__getattribute__('c' + color.id)
        color.inputs = [choice for choice in color.input]
    return form
