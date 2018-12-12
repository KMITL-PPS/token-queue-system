import logging

from flask_jwt import JWT
from flask_login import LoginManager
from passlib.hash import bcrypt

from tqs import app
from tqs.models import Manager


# JWT
def identity(payload):
    manager_id = payload['identity']
    return Manager.query.get(manager_id)

def auth_user(username: str, password: str):
    # get user
    manager = Manager.query.filter(Manager.username == username).first()
    # verify password if user is exists
    if manager is not None and bcrypt.verify(password, manager.password):
        return manager
    return None

# init jwt
jwt = JWT(app, auth_user, identity)

# init login manager
with app.app_context():
    login_manager = LoginManager()
    login_manager.init_app(app)
