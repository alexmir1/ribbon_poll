"""
db models
"""


from app import db


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.String(128))
    hex = db.Column(db.String(8))

    marks = db.relationship('Mark', backref='color', lazy='dynamic')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    grade = db.Column(db.String(4), index=True, nullable=False)

    marks = db.relationship('Mark', backref='user', lazy='dynamic')


class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
