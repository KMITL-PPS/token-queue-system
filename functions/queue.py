import json

from functions.config import increase_read_config, read_config, write_config, decrease_read_config


def reset_queue():
    write_config('total_queue', 0)
    write_config('current_queue', 0)


def create_queue() -> str:
    queue = increase_read_config('total_queue')
    if queue is None:  # error occurred
        return None

    return queue


def get_queue() -> int:
    return read_config('current_queue')


def total_queue() -> int:
    return read_config('total_queue')


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
