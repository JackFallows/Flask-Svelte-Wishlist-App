import json
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from data_access.models.wishlist import Wishlist
from data_access.models.wishlist_item import WishlistItem

wishlist_items = Blueprint('wishlist_items', __name__)

@login_required
@wishlist_items.route('/get_all_for_wishlist/<wishlist_id>')
def get_all_for_wishlist(wishlist_id):
    user_id = current_user.id
    
    wishlist = Wishlist.get(wishlist_id=wishlist_id, user_id=user_id)
    if wishlist is None:
        return "Not found", 404
    
    wishlist_items = WishlistItem.get_all_for_wishlist(wishlist_id=wishlist_id)
    
    return jsonify(list(map(lambda w: w.as_dict(), wishlist_items)))

@login_required
@wishlist_items.route('/post', methods=["POST"])
def post_wishlist_item():
    wishlist_item = json.loads(request.data)
    
    wishlist = Wishlist.get(wishlist_item['wishlist_id'], current_user.id)
    
    if (wishlist is None):
        return "Not found", 404
    
    # TODO validation
    
    wishlist_item_id = WishlistItem.create(wishlist_id=wishlist.id, link=wishlist_item['link'], notes=wishlist_item['notes'])
    
    return jsonify(id=wishlist_item_id)
