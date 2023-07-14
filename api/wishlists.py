import json
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from data_access.models.wishlist import Wishlist

wishlists = Blueprint('wishlists', __name__)

@login_required
@wishlists.route('/get/<wishlist_id>')
def get_wishlist(wishlist_id):
    if wishlist_id == None:
        return jsonify({})
    
    wishlist = Wishlist.get(wishlist_id=wishlist_id, user_id=current_user.id)
    
    return jsonify(wishlist.as_dict())

@login_required
@wishlists.route('/get_all_for_user')
def get_all_for_user():
    user_id = current_user.id
    
    wishlists = Wishlist.get_all_for_user(user_id=user_id)
    
    return jsonify(list(map(lambda w: w.as_dict(), wishlists)))

@login_required
@wishlists.route('/post', methods=["POST"])
def post_wishlist():
    wishlist = json.loads(request.data)
    
    # TODO validation
    
    wishlist_id = Wishlist.create(name=wishlist['name'], user_id=current_user.id)
    
    return jsonify(id=wishlist_id)
