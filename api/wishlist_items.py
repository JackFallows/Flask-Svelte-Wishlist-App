import json
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from data_access.models.wishlist import Wishlist
from data_access.models.wishlist_item import WishlistItem
from services.notification_service import notify_wishlist_updated

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
@wishlist_items.route('/create', methods=["POST"])
def create():
    wishlist_item_json = json.loads(request.data)
    wishlist_item = WishlistItem.from_json(wishlist_item_json)
    
    wishlist = Wishlist.get(wishlist_id=wishlist_item.wishlist_id, user_id=current_user.id)
    if wishlist is None:
        return "Not found", 404
    
    WishlistItem.increment_order_numbers_from(wishlist_item.wishlist_id, wishlist_item.order_number)
    
    wishlist_item_id = WishlistItem.create(
            wishlist_id=wishlist_item.wishlist_id,
            link=wishlist_item.link,
            notes=wishlist_item.notes,
            order_number=wishlist_item.order_number,
            is_header=wishlist_item.is_header)
    
    if not wishlist_item.is_header:
        notify_wishlist_updated(current_user, wishlist)
    
    return jsonify({
        "wishlist_item_id": wishlist_item_id
    })

@login_required
@wishlist_items.route('/change-text/<wishlist_item_id>', methods=["PATCH"])
def change_text(wishlist_item_id):
    if not WishlistItem.get_is_available_to_user(wishlist_item_id=wishlist_item_id, user_id=current_user.id):
        return "Not found", 404
    
    wishlist_text = json.loads(request.data)
    
    name = wishlist_text["name"]
    description = wishlist_text["description"]
    
    WishlistItem.set_item_text(wishlist_item_id, name, description)
    
    return jsonify({})
    

@login_required
@wishlist_items.route('/mark-as-bought/<wishlist_item_id>', methods=["PATCH"])
def mark_as_bought(wishlist_item_id):
    if not WishlistItem.get_is_available_to_user(wishlist_item_id=wishlist_item_id, user_id=current_user.id):
        return "Not found", 404
    
    WishlistItem.set_as_bought(wishlist_item_id=wishlist_item_id)
    
    return jsonify({})

@wishlist_items.route('/link_share_mark_bought/<share_guid>/<wishlist_item_id>', methods=["PATCH"])
def link_share_mark_bought(share_guid, wishlist_item_id):
    if not WishlistItem.get_is_available_to_link_share(wishlist_item_id, share_guid):
        return "Not found", 404
    
    WishlistItem.set_as_bought(wishlist_item_id=wishlist_item_id)
    
    return jsonify({})

@login_required
@wishlist_items.route('/reparent/<wishlist_item_id>/<target_wishlist_id>', methods=["PATCH"])
def reparent(wishlist_item_id, target_wishlist_id):
    if not WishlistItem.get_is_owned_by_user(wishlist_item_id, user_id=current_user.id):
        return "Not found", 404
    
    target_wishlist = Wishlist.get(target_wishlist_id, user_id=current_user.id)
    
    if not target_wishlist:
        return "Not found", 404
    
    WishlistItem.reparent(wishlist_item_id, target_wishlist_id)
    
    return jsonify({})

@login_required
@wishlist_items.route('/ensure-order/<wishlist_id>', methods=["PATCH"])
def ensure_order(wishlist_id):
    wishlist = Wishlist.get(wishlist_id, current_user.id)
    if not wishlist:
        return "Not found", 404
    
    wishlist_items_json = json.loads(request.data)
    
    for item in wishlist_items_json:
        WishlistItem.set_order_number(item["wishlist_item_id"], item["order_number"])
        
    return jsonify({})

@login_required
@wishlist_items.route('/delete/<wishlist_item_id>', methods=["DELETE"])
def delete_item(wishlist_item_id):
    if not WishlistItem.get_is_owned_by_user(wishlist_item_id, user_id=current_user.id):
        return "Not found", 404
    
    WishlistItem.remove(wishlist_item_id)
    
    return jsonify({})
