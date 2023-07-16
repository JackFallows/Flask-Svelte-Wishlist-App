from flask import Blueprint
from flask_login import login_required

from helpers import custom_render_template

edit = Blueprint('edit', __name__)

@edit.route('/')
@edit.route('/<wishlist_id>')
@login_required
def edit_wishlist(wishlist_id=0):
    return custom_render_template("edit_wishlist.html", wishlist_id=None if wishlist_id == 0 else wishlist_id)

