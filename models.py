from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
