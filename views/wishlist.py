from flask import Blueprint
from flask_login import login_required

from helpers import custom_render_template

wishlist = Blueprint('wishlist', __name__)

@wishlist.route('/view/<wishlist_id>')
@login_required
def view_wishlist(wishlist_id):
    return custom_render_template("view_wishlist.html", wishlist_id=wishlist_id)

@wishlist.route('/create')
@wishlist.route('/edit/<wishlist_id>')
@login_required
def edit_wishlist(wishlist_id=0):
    return custom_render_template("edit_wishlist.html", wishlist_id=None if wishlist_id == 0 else wishlist_id)

