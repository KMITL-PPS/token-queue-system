import json
import logging

from tqs import app, db
from tqs.functions.config import decrease_read_config, increase_read_config, \
    read_config, write_config
from tqs.functions.key import get_key_id
from tqs.models import Queue


logger = logging.getLogger('flask.app.queue')


def reset_queue():
    write_config('total_queue', 0)
    write_config('current_queue', 0)


def create_queue() -> str:
    queue = increase_read_config('total_queue')

    # save to db
    queue_obj = Queue(
        key=get_key_id(),
        queue=queue
    )
    db.session.add(queue_obj)
    db.session.commit()

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

    # save to db
    key = get_key_id()
    queue_obj = Queue.query.filter_by(
        key=key,
        queue=queue
    ).first()

    if queue_obj is not None:
        queue_obj.used = True
        db.session.commit()
    else:
        logger.error(f'Cannot find queue object (key={key}, queue={queue})')

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
