import os

ENABLE_INTERNAL_AUTH = os.environ.get("ENABLE_INTERNAL_AUTH", None)

def enable_internal_auth(func):
    def inner():
        if (ENABLE_INTERNAL_AUTH is None or ENABLE_INTERNAL_AUTH.lower() == 'false'):
            return "Not found", 404
        return func()
    inner.__name__ = func.__name__ # make sure Flask doesn't complain
    return inner
