from aiogram.types import *
import logging

def log(message: str):
    def make_log(func):
        def wrapper(*args, user: User, **kwargs):
            result = func(*args, **kwargs)
            logging.info(f'<{user.id}> {message}')
            return result
        return wrapper
    return make_log