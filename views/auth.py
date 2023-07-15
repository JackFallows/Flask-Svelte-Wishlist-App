import json
import os

from flask import Blueprint, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
from oauthlib.oauth2 import WebApplicationClient
import requests

from data_access.models.user import User

auth = Blueprint('auth', __name__)

@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
