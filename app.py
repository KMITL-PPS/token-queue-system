import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from passlib.hash import bcrypt

from forms import LoginForm
from functions.config import load_config
from functions.key import load_key
from functions.qr import generate_qr
from functions.queue import create_queue, remaining_queue
from models import Manager, db


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

@app.route('/')
def index():
    return render_template('customerQueue.html', queue_remain=remaining_queue())

@app.route('/qr')
def qr():
    queue = create_queue()
    qr_code = generate_qr(queue)
    return render_template('customerQR.html', queue_remain=remaining_queue(), customer_queue=queue, qr=qr_code)

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

@app.route('/admin')
@login_required
def admin():
    return render_template('adminQueue.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
