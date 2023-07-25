import json

from functools import wraps
from flask import request, jsonify

def validate(validator):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            request_json = json.loads(request.data)
            state = validator(request_json)
            if not state.is_valid:
                return jsonify(state.as_dict()), 403
            return func(*args, **kwargs)
        return inner
    return decorator
