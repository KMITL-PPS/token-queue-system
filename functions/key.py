import json
from collections import OrderedDict

from cryptography.fernet import Fernet

from functions.config import read_config, write_config


suite = None


def load_key():
    global suite
    key = read_config('key')
    if key is None or key == '':
        generate_key()
    else:
        suite = Fernet(key.encode())


def generate_key(reload: bool = True):
    global suite
    new_key = Fernet.generate_key()
    write_config('key', new_key.decode())
    if reload:
        suite = Fernet(new_key)


def encrypt(data) -> str:
    if suite is None:  # error occurred
        return None
    return suite.encrypt(str(data).encode()).decode()


def decrypt(data: str):
    if suite is None:  # error occurred
        return None

    decrypted_data = suite.decrypt(data.encode()).decode()
    if decrypted_data.isdigit():
        return int(decrypted_data)
    return decrypted_data
