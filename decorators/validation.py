import json

from functools import wraps
from flask import request, jsonify

from validators.user import validate

def validate_user(func):
    @wraps(func)
    def inner(*args, **kwargs):
        request_json = json.loads(request.data)
        valid, message = validate(request_json)
        if not valid:
            return jsonify({ "error": message }), 403
        return func(*args, **kwargs)
    return inner
