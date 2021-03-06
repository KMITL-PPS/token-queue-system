from getpass import getpass

from passlib.hash import bcrypt

from tqs import app, db
from tqs.models import Manager


@app.cli.command()
def init_db():
    db.create_all()
    print('Success!')


@app.cli.command()
def create_manager():
    alias = input('Alias: ')
    username = input('Username: ')
    password_input = getpass('Password: ')
    password_confirm_input = getpass('Password (again): ')

    # check two password
    if password_input != password_confirm_input:
        print('Password do not match!')
        exit(0)

    # encrypt password
    password = bcrypt.hash(password_input)

    # create and commit model
    manager = Manager(alias=alias, username=username, password=password)
    db.session.add(manager)
    db.session.commit()

    print('Success!')
