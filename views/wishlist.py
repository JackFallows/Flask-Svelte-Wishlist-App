from flask import Blueprint
from flask_login import login_required

from helpers import custom_render_template

wishlist = Blueprint('wishlist', __name__)

@wishlist.route('/')
@wishlist.route('/<wishlist_id>')
@login_required
def view_wishlist2(wishlist_id=0):
    return custom_render_template("wishlist.html", wishlist_id=wishlist_id)
