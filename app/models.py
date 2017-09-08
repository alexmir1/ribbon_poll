"""
db models
"""


from app import db


class Colors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_color = db.Column(db.String(64), index=True)
    background_color = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Color %r>' % self.id
