import os

from flask_login import current_user

ENABLE_INTERNAL_AUTH = os.environ.get("ENABLE_INTERNAL_AUTH", None)

def enable_internal_auth(func):
    def inner():
        if (ENABLE_INTERNAL_AUTH is None or ENABLE_INTERNAL_AUTH.lower() == 'false'):
            return "Not found", 404
        return func()
    inner.__name__ = func.__name__ # make sure Flask doesn't complain
    return inner

def logout_required(func):
    def inner():
        if current_user.is_authenticated:
            return "Forbidden", 403
        return func()
    inner.__name__ = func.__name__
    return inner
