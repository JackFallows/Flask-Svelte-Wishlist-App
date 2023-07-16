from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, logout_user, current_user

from decorators import enable_internal_auth

auth = Blueprint('auth', __name__)

@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@auth.route("/sign-up")
@enable_internal_auth
def sign_up():
    return render_template("sign_up.html", user=current_user)

@auth.route("/login")
@enable_internal_auth
def login():
    return render_template("login.html", user=current_user)
