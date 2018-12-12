import json

from tqs import app
from tqs.functions.config import decrease_read_config, increase_read_config, \
    read_config, write_config


def reset_queue():
    write_config('total_queue', 0)
    write_config('current_queue', 0)


def create_queue() -> str:
    queue = increase_read_config('total_queue')
    # TODO: insert to db
    return queue


def get_queue() -> int:
    return read_config('current_queue')


def total_queue() -> int:
    return read_config('total_queue')


def get_queue_status(queue: int) -> str:
    current_queue = get_queue()
    if queue == current_queue:
        return 'current'
    elif queue < current_queue:
        return 'passed'
    return 'not yet'


def can_next_queue() -> bool:
    return get_queue() < total_queue()


def next_queue() -> int:
    if not can_next_queue():
        return None  # no next queue

    queue = increase_read_config('current_queue')
    return queue


def previous_queue() -> int:
    if get_queue() <= 0:
        return None  # no previous queue

    queue = decrease_read_config('current_queue')
    return queue


def remaining_queue() -> int:
    total_queue = read_config('total_queue')
    current_queue = read_config('current_queue')

    remaining_queue = total_queue - current_queue
    return remaining_queue
