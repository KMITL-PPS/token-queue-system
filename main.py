from flask import Flask, render_template

from functions.key import load_key
from functions.queue import create_queue, get_queue


app = Flask(__name__)
load_key()

@app.route('/')
def hello():
    return render_template('index.html', name=create_queue())

@app.route('/decode/<token>')  # test purpose only
def decode(token):
    return render_template('index.html', name=get_queue(token))
