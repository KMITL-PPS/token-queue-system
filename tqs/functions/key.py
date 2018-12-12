import json
from collections import OrderedDict
from json import JSONDecodeError

from cryptography.fernet import Fernet, InvalidToken, InvalidSignature

from tqs.functions.config import read_config, write_config


suite = None


def load_key():
    global suite
    key = read_config('key')
    if key is None or key == '':
        set_key(key=generate_key())
    else:
        suite = Fernet(key.encode())


def generate_key(decoded: bool = False):
    key = Fernet.generate_key()
    return key.decode() if decoded else key


def get_key_id():
    key = read_config('key')
    return key[:3]


def set_key(key, reload: bool = True):
    write_config('key', key.decode())
    if reload:
        suite = Fernet(key)


def encrypt(data) -> str:
    if suite is None:  # error occurred
        return None
    return suite.encrypt(str(data).encode()).decode()


def decrypt(data: str):
    if suite is None:  # error occurred
        return None

    try:
        decrypted_data = suite.decrypt(data.encode()).decode()
    except InvalidToken:
        raise Exception('Invalid token.')
    except InvalidSignature:
        raise Exception('Invalid signature.')

    if decrypted_data.isdigit():
        return int(decrypted_data)
    try:
        return json.loads(decrypted_data)
    except JSONDecodeError:
        pass
    return decrypted_data
