import os

from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from passlib.hash import bcrypt

from forms import LoginForm
from functions.config import load_config
from functions.key import generate_key, load_key, set_key
from functions.qr import generate_qr
from functions.queue import can_next_queue, create_queue, get_queue, \
    next_queue, previous_queue, remaining_queue, reset_queue
from models import Manager, db


app = Flask(__name__)

# load environment
load_dotenv()
queue_interval = os.environ.get('QUEUE_INTERVAL', 5000)

# app config
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'CHANGE THIS'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DB_URI', 'sqlite:///{}'.format(db_path)),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

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
def load_user(user_id):
    return Manager.query.get(user_id)


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

    # submit form
    if form.validate_on_submit():
        # get user
        manager = Manager.query.filter(Manager.username == form.username.data).first()

        # verify password if user is exists
        if manager is not None and bcrypt.verify(form.password.data, manager.password):
            login_user(manager)
            flash('Log in successfully!')
            return redirect(url_for('admin'))
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
