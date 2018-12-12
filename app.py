import json
import os
import traceback

import logging.config
from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, \
    url_for
from flask_jwt import JWT, jwt_required
from flask_login import LoginManager, login_required, login_user, logout_user
from passlib.hash import bcrypt

from forms import LoginForm
from functions.config import load_config
from functions.key import decrypt, generate_key, load_key, set_key
from functions.qr import generate_qr
from functions.queue import can_next_queue, create_queue, get_queue, \
    get_queue_status, next_queue, previous_queue, remaining_queue, \
    reset_queue
from models import Log, Manager, db


# load flask
app = Flask(__name__)

# load environment
load_dotenv()

# app config
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'CHANGE THIS'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DB_URI', 'sqlite:///{}'.format(db_path)),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# init db
with app.app_context():
    db.app = app
    db.init_app(app)

# load logger
class SQLAlchemyHandler(logging.StreamHandler):
    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
        log = Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            message=record.__dict__['msg'],)
        db.session.add(log)
        db.session.commit()

db_handler = SQLAlchemyHandler()
db_handler.setLevel(logging.INFO)
app.logger.handlers[0].setLevel(logging.WARNING)
app.logger.addHandler(db_handler)
app.logger.setLevel(logging.INFO)

# load setting
queue_interval = os.environ.get('QUEUE_INTERVAL', 5000)

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

# init app
with app.app_context():
    # database
    db.app = app
    db.init_app(app)

    # login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

# load config/key
load_config()
load_key()


@login_manager.user_loader
def load_user(manager_id: int):
    return Manager.query.get(manager_id)


@app.route('/', methods=['GET'])
def index():
    return render_template('customerQueue.html', queue_remain=remaining_queue())


@app.route('/qr', methods=['GET'])
def qr():
    queue = create_queue()
    qr_code = generate_qr(queue)
    return render_template('customerQR.html', queue_remain=remaining_queue() - 1, customer_queue=queue, qr=qr_code)


@app.route('/login', methods=['GET', 'POST'])
def _login():
    form = LoginForm()

    # submit form (POST)
    if form.validate_on_submit():
        # authenticate user
        manager = auth_user(username=form.username.data, password=form.password.data)
        if manager is not None:
            login_user(manager)
            app.logger.info(f'Manager `{manager.alias}` logged in.')
            flash('Log in successfully!')
            return redirect(url_for('admin'))
        app.logger.info(f'Attempt to log in with username `{form.username.data}`.')
        flash('Invalid username or password!')

    # GET
    return render_template('login.html', form=form)


@app.route('/admin', methods=['GET'])
@login_required
def admin():
    return render_template('adminQueue.html', queue=get_queue(), interval=queue_interval)


@app.route('/queue/any-next', methods=['GET'])
@login_required
def queue_any_next():
    return jsonify(next=can_next_queue())


@app.route('/queue/next', methods=['GET'])
@login_required
def queue_next():
    queue = next_queue()
    if queue is None:
        flash('Cannot change queue!')
    return redirect(url_for('admin'))


@app.route('/queue/previous', methods=['GET'])
@login_required
def queue_previous():
    queue = previous_queue()
    if queue is None:
        flash('Cannot change queue!')
    return redirect(url_for('admin'))


@app.route('/queue/reset', methods=['GET'])
@login_required
def queue_reset():
    reset_queue()
    new_key = generate_key()
    set_key(new_key, reload=True)
    return redirect(url_for('admin'))


@app.route('/queue/verify', methods=['POST'])
# @login_required
@jwt_required()
def queue_verify():
    data = json.loads(request.data)
    data = data['data']

    # decrypt data and prepare response
    try:
        response_data = decrypt(data)
    except Exception as e:
        response_data = {
            'error': 'Error',
            'description': str(e)
        }
        return jsonify(response_data), 400

    # get queue status
    queue_status = get_queue_status(response_data['queue'])
    if queue_status == 'current':
        response_data['valid'] = True
    else:
        response_data['valid'] = False
        response_data['status'] = queue_status

    return jsonify(response_data)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('_login'))


if __name__ == '__main__':
    app.run()
