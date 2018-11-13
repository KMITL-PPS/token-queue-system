import json

from functions.config import increase_read_config, write_config
from functions.key import decrypt, encrypt, generate_key


def reset_queue(regenerate_key: bool = True):
    write_config('total_queue', 0)
    write_config('current_queue', 0)
    if regenerate_key:
        generate_key()


def create_queue() -> str:
    queue = increase_read_config('total_queue')
    if queue is None:  # error occurred
        return None

    return encrypt(queue)


def get_queue(token: str) -> int:
    return decrypt(token)


def next_queue() -> int:
    queue = increase_read_config('current_queue')
    if queue is None:  # error occurred
        return None

    return queue
