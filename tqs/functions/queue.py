import json
import logging

from flask_login import current_user

from tqs import app
from tqs.functions.config import decrease_read_config, increase_read_config, \
    read_config, write_config


logger = logging.getLogger('flask.app.queue')


def reset_queue():
    write_config('total_queue', 0)
    write_config('current_queue', 0)

    logger.info(f'Manager `{current_user.alias}` reset queue.')


def create_queue() -> str:
    queue = increase_read_config('total_queue')
    # TODO: insert to db
    logger.info(f'Created queue #{queue}.')
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
    if queue is None:  # error occurred
        return None

    return queue


def previous_queue() -> int:
    if get_queue() <= 0:
        return None  # no previous queue

    queue = decrease_read_config('current_queue')
    if queue is None:  # error occurred
        return None

    return queue


def remaining_queue() -> int:
    total_queue = read_config('total_queue')
    current_queue = read_config('current_queue')

    remaining_queue = total_queue - current_queue
    return remaining_queue
