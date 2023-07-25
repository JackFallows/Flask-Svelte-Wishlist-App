import json
import uuid

from flask import Blueprint, jsonify, request
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from data_access.models.user import User
from decorators.auth import enable_internal_auth
from decorators.validation import validate_user

users = Blueprint('users', __name__)

@enable_internal_auth
@users.route("/create", methods=["POST"])
@validate_user
def sign_up():
    request_json = json.loads(request.data)
    
    User.create(
        id_=str(uuid.uuid4()),
        name=request_json['name'],
        email=request_json['email'],
        profile_pic=None,
        internal_password=generate_password_hash(request_json['password1'], method='scrypt'))

    return jsonify({})

@enable_internal_auth
@users.route("/authenticate", methods=["POST"])
def login():
    request_json = json.loads(request.data)
    
    user = User.get_by_email(email=request_json["email"])
    if user is None or not check_password_hash(user.internal_password, request_json["password"]):
        return "Forbidden", 403
    
    login_user(user)
    return jsonify({})
