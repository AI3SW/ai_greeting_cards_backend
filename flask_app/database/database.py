from datetime import datetime, timezone

from flask_app.database import db


def get_default_utc_timestamp():
    return datetime.now(timezone.utc)


class InputImg(db.Model):
    __tablename__ = "input_img"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_path = db.Column(db.Text)
    created_date = db.Column(db.DateTime(timezone=True),
                             default=get_default_utc_timestamp)

    def __repr__(self) -> str:
        return '<InputImg FILE_PATH %r' % self.file_path


class OutputImg(db.Model):
    __tablename__ = "output_img"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_path = db.Column(db.Text)
    created_date = db.Column(db.DateTime(timezone=True),
                             default=get_default_utc_timestamp)

    def __repr__(self) -> str:
        return '<OutputImg> FILE_PATH %r' % self.file_path


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    img_path = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Job NAME> %r>' % self.name


class User(db.Model):
    id = db.Column(db.Text, primary_key=True)
    sessions = db.relationship('Session', backref='user', lazy=True)

    def __repr__(self) -> str:
        return '<User> ID %r' % self.id


class Version(db.Model):
    version = db.Column(db.Text, primary_key=True)

    def __repr__(self) -> str:
        return '<Version> VERSION %r' % self.version


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Text, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    input_img_id = db.Column(db.Integer, db.ForeignKey('input_img.id'))
    output_img_id = db.Column(db.Integer, db.ForeignKey('output_img.id'))
    start_time = db.Column(db.DateTime(timezone=True),
                           default=get_default_utc_timestamp)
    end_time = db.Column(db.DateTime(timezone=True),
                         default=get_default_utc_timestamp)

    def __repr__(self) -> str:
        return '<Session> ID %r' % self.id
