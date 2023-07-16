from flask import Blueprint, redirect, url_for
from flask_login import login_required, logout_user

from decorators import enable_internal_auth
from helpers import custom_render_template

auth = Blueprint('auth', __name__)

@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@auth.route("/sign-up")
@enable_internal_auth
def sign_up():
    return custom_render_template("sign_up.html")

@auth.route("/login")
@enable_internal_auth
def login():
    return custom_render_template("login.html")
