import json
import logging
import logging.config
import os

from flask import flash, jsonify, redirect, render_template, request, session, \
    url_for
from flask_jwt import jwt_required
from flask_login import LoginManager, login_required, login_user, logout_user, \
    current_user

from tqs import app, logging
from tqs.auth import login_manager, auth_user
from tqs.commands import create_manager, init_db
from tqs.forms import LoginForm
from tqs.functions.config import load_config
from tqs.functions.key import decrypt, generate_key, load_key, set_key, get_key_id
from tqs.functions.qr import generate_qr
from tqs.functions.queue import can_next_queue, create_queue, get_queue, \
    get_queue_status, next_queue, previous_queue, remaining_queue, \
    reset_queue
from tqs.models import Log, Manager


# load setting
queue_interval = os.environ.get('QUEUE_INTERVAL', 5000)

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
    key_id = get_key_id()
    if session.get('key_id', None) == key_id and session.get('queue', None) >= get_queue():  #TODO: implement using db
        queue = session.get('queue', None)
    else:
        queue = create_queue()

        # save to session
        session['key_id'] = key_id
        session['queue'] = queue

        app.logger.info(f'Created queue. (queue={queue}, key={key_id})')

    qr_code = generate_qr(queue)

    return render_template('customerQR.html', queue_remain=remaining_queue() - 1, customer_queue=queue, qr=qr_code)


@app.route('/login', methods=['GET', 'POST'])
def _login():
    error = None
    form = LoginForm()

    # submit form (POST)
    if form.validate_on_submit():
        # authenticate user
        manager = auth_user(username=form.username.data, password=form.password.data)
        if manager is not None:
            login_user(manager)

            app.logger.info(f'Manager `{manager.alias}` logged in.')
            return redirect(url_for('admin'))

        app.logger.info(f'Attempt to log in with username `{form.username.data}`.')
        error = 'Invalid username or password!'

    # GET
    return render_template('login.html', form=form, error=error)


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

    app.logger.info(f'Manager `{current_user.alias}` moved to next queue. (queue={queue}, key={get_key_id()})')
    return redirect(url_for('admin'))


@app.route('/queue/previous', methods=['GET'])
@login_required
def queue_previous():
    queue = previous_queue()

    app.logger.info(f'Manager `{current_user.alias}` moved to previous queue. (queue={queue}, key={get_key_id()})')
    return redirect(url_for('admin'))


@app.route('/queue/reset', methods=['GET'])
@login_required
def queue_reset():
    reset_queue()
    new_key = generate_key()
    set_key(new_key, reload=True)

    app.logger.warning(f'Manager `{current_user.alias}` reset queue. (key={get_key_id()})')
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
        app.logger.warning(f'Manager `{current_user.alias} failed to verify QR code (data={data})`', exc_info=1)

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
    app.logger.info(f'Manager `{current_user.alias}` logged out.')

    logout_user()
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized():
    app.logger.warning('Attempted request to unauthorized page.')
    return redirect(url_for('_login'))


if __name__ == '__main__':
    app.run()
