from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Manager(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Queue(db.Model):
    __table_args__ = (
        db.UniqueConstraint('key', 'queue', name='unique_key_queue'),
    )

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(3))
    queue = db.Column(db.Integer)
    issue_dt = db.Column(db.DateTime, default=datetime.now)
    used = db.Column(db.Boolean, default=False)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logger = db.Column(db.String)
    level = db.Column(db.String)
    trace = db.Column(db.String)
    message = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.now)
