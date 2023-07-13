from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user

from data_access.models.wishlist import Wishlist

edit = Blueprint('edit', __name__)

@edit.route('/')
@edit.route('/<wishlist_id>')
@login_required
def edit_wishlist(wishlist_id=0):
    return render_template("edit_wishlist.html", user=current_user, wishlist_id=None if wishlist_id == 0 else wishlist_id)

