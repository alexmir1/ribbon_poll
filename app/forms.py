from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import NumberRange


class ColorMark(Form):
    mark = StringField('Mark', validators=[NumberRange(1, 100, 'А ещё в матклассе учишься!')])
