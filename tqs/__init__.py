import os

from dotenv import load_dotenv
from flask import Flask

from tqs.models import db


# load flask
app = Flask(__name__)

# load environment
load_dotenv()

# app config
db_path = os.path.join(os.path.dirname(__file__), '../app.db')
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'CHANGE THIS'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DB_URI', 'sqlite:///{}'.format(db_path)),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# init db
with app.app_context():
    db.app = app
    db.init_app(app)

from tqs import commands, logging, views, utils

if __name__ == '__main__':
    app.run()
