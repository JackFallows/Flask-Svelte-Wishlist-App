import json
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from data_access.models.wishlist import Wishlist
from data_access.models.wishlist_item import WishlistItem

wishlists = Blueprint('wishlists', __name__)

@login_required
@wishlists.route('/get/<wishlist_id>')
def get_wishlist(wishlist_id):
    if wishlist_id == None:
        return jsonify({})
    
    wishlist = Wishlist.get(wishlist_id=wishlist_id, user_id=current_user.id)
    wishlist_items = WishlistItem.get_all_for_wishlist(wishlist_id=wishlist.id)
    
    wishlist_merged = { **wishlist.as_dict(), **{ "wishlist_items": list(map(lambda wi: wi.as_dict(), wishlist_items)) } }
    
    return jsonify(wishlist_merged)

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
    
    wishlist_items = list(map(lambda wi: WishlistItem.from_json(wi), wishlist['wishlist_items']))
    
    for wishlist_item in wishlist_items:
        WishlistItem.create(
            wishlist_id=wishlist_id,
            link=wishlist_item.link,
            notes=wishlist_item.notes,
            order_number=wishlist_item.order_number)
    
    return jsonify(id=wishlist_id)

@login_required
@wishlists.route('/put', methods=["PUT"])
def put_wishlist():
    wishlist_json = json.loads(request.data)
    
    wishlist = Wishlist.from_json(wishlist_json)
    wishlist_items = list(map(lambda wi: WishlistItem.from_json(wi), wishlist_json['wishlist_items']))
    
    db_wishlist = Wishlist.get(wishlist_id=wishlist.id, user_id=current_user.id)
    
    if db_wishlist is None:
        return "Not found", 404
    
    if len(list(filter(lambda wi: wi.wishlist_id is not None and wi.wishlist_id != wishlist.id, wishlist_items))) != 0:
        # there are items belonging to different wishlists
        return "Not found", 404
    
    # TODO validation
    
    wishlist.apply_changes()
    
    existing_item_ids = WishlistItem.get_ids_for_wishlist(wishlist_id=wishlist.id)
    saving_ids = list(map(lambda item: item.id, filter(lambda item: item.id is not None, wishlist_items)))
    
    ids_to_remove = list(filter(lambda existing_id: existing_id not in saving_ids, existing_item_ids))
    
    for id_to_remove in ids_to_remove:
        WishlistItem.remove(wishlist_item_id=id_to_remove)
    
    for wishlist_item in wishlist_items:
        if wishlist_item.id is None:
            WishlistItem.create(
                wishlist_id=wishlist.id,
                link=wishlist_item.link,
                notes=wishlist_item.notes,
                order_number=wishlist_item.order_number)
        else:
            wishlist_item.apply_changes()
            
    return jsonify({})
