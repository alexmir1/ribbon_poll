from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class ColorPickers(Form):
    text_color = StringField('text_color', validators=[DataRequired()], default='black')
    background_color = StringField('background_color', validators=[DataRequired()], default='white')
