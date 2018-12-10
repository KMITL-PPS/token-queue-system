import os
from dotenv import load_dotenv
from flask import Flask, render_template

from functions.key import load_key
from functions.queue import create_queue, get_queue
from models import db


app = Flask(__name__)

# load environment
load_dotenv()

# app config
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'CHANGE THIS'),
    ENV=os.environ.get('ENV', 'development'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DB_URI', 'sqlite:///{}'.format(db_path)),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# database
db.init_app(app)

# load key
try:
    load_key()
except PermissionError:
    print('You need to run with root permission only!')
    exit(0)

@app.route('/')
def index():
    return render_template('customerQueue.html')

@app.route('/qr')
def qr_page():
    return render_template('customerQR.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/admin')
def admin_page():
    return render_template('adminQueue.html')

@app.route('/decode/<token>')  # test purpose only
def decode(token):
    return render_template('index.html', name=get_queue(token))

if __name__ == '__main__':
    app.run()
