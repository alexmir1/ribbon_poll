from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField


class Feedback(FlaskForm):
    usability = StringField('usability')
    usefulness = StringField('usefulness')
    designing = StringField('designing')
    comment = TextAreaField('comment')
