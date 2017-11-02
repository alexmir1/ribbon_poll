"""
db models
    """


from app import db


class Color(db.Model):
    """
    Цвет
    """
    id = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.String(128), unique=True)
    hex = db.Column(db.String(8), nullable=False)

    marks = db.relationship('Mark', backref='color', lazy='dynamic')


class User(db.Model):
    """
    Пользователь
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    grade = db.Column(db.String(4), index=True, nullable=False)
    name = db.Column(db.String(64), unique=True, nullable=False)
    feedback_count = db.Column(db.Integer, nullable=False, default=0)

    marks = db.relationship('Mark', backref='user', lazy='dynamic')
    choices = db.relationship('Choices', backref='user', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)


class Mark(db.Model):
    """
    Старые оценки от 1 до 100.
    Нужны чтобы пользователям, поставившим всем цветам различные оценки не нужно было ничего делать.
    """
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)


class Round(db.Model):
    """
    Раунд голосования
    """
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(4), index=True, nullable=False)
    starts_at = db.Column(db.DateTime)

    previous_id = db.Column(db.Integer, db.ForeignKey('round.id'))
    previous = db.relationship('Round', backref='next', uselist=False, remote_side=[id])
    current = db.relationship('CurrentRound', backref='round', lazy='dynamic')
    colors = db.relationship('ComparingColors', backref='round', lazy='dynamic')


class CurrentRound(db.Model):
    """
    id текущих раундов
    """
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(4), index=True, nullable=False, unique=True)

    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)


class ComparingColors(db.Model):
    """
    Пара сравниваемых цветов
    """
    id = db.Column(db.Integer, primary_key=True)
    first_color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
    second_color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=True)

    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False, index=True)
    first_color = db.relationship('Color', uselist=False, foreign_keys=[first_color_id])
    second_color = db.relationship('Color', uselist=False, foreign_keys=[second_color_id])
    choices = db.relationship('Choices', backref='comparing_colors', lazy='dynamic')


class Choices(db.Model):
    """
    Выбор пользователей
    """
    id = db.Column(db.Integer, primary_key=True)
    selected = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comparing_colors_id = db.Column(db.Integer, db.ForeignKey('comparing_colors.id'), nullable=False)
