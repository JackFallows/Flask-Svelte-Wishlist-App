import os
from functools import wraps

from flask_login import current_user

ENABLE_INTERNAL_AUTH = os.environ.get("ENABLE_INTERNAL_AUTH", None)

def enable_internal_auth(func):
    @wraps(func)
    def inner():
        if (ENABLE_INTERNAL_AUTH is None or ENABLE_INTERNAL_AUTH.lower() == 'false'):
            return "Not found", 404
        return func()
    return inner

def logout_required(func):
    @wraps(func)
    def inner():
        if current_user.is_authenticated:
            return "Forbidden", 403
        return func()
    return inner
