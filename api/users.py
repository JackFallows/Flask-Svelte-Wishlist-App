import json
import uuid

from flask import Blueprint, jsonify, request
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from data_access.models.user import User
from decorators.auth import enable_internal_auth
from decorators.validation import validate

from validators.user import validate_create as user_create_validator

users = Blueprint('users', __name__)

@enable_internal_auth
@users.route("/create", methods=["POST"])
@validate(user_create_validator)
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

@users.route('/get')
@login_required
def get():
    user = User.get(current_user.id)
        
    if user == None:
        return "Not found", 404
    
    return jsonify(user.as_dict())

@users.route("/update", methods=["PATCH"])
@login_required
#@validate(user_update_validator)
def update():
    request_json = json.loads(request.data)
    
    user = User.get(current_user.id)
    
    user.email_on_share = request_json["email_on_share"]
    user.email_on_update = request_json["email_on_update"]
    
    user.apply_changes()

    return jsonify({})
