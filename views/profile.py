from flask import Blueprint
from flask_login import login_required

from helpers import custom_render_template

profile = Blueprint('profile', __name__)

@profile.route('/')
@login_required
def view_wishlist():
    return custom_render_template("profile.html")
