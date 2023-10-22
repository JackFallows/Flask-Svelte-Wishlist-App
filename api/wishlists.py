import json
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from data_access.models.user import User
from data_access.models.wishlist import Wishlist
from data_access.models.wishlist_share import WishlistShare
from data_access.models.wishlist_item import WishlistItem
from data_access.models.user_shared_wishlist import UserSharedWishlist

from services.notification_service import notify_wishlist_shared, notify_wishlist_updated

wishlists = Blueprint('wishlists', __name__)

@login_required
@wishlists.route('/get/<wishlist_id>')
def get_wishlist(wishlist_id):
    if wishlist_id == None:
        return jsonify({})
    
    wishlist = Wishlist.get(wishlist_id=wishlist_id, user_id=current_user.id)
    if wishlist == None:
        wishlist = WishlistShare.get(user_id=current_user.id, wishlist_id=wishlist_id)
        
    if wishlist == None:
        return "Not found", 404
    
    wishlist_items = WishlistItem.get_all_for_wishlist(wishlist_id=wishlist.id)
    
    wishlist_merged = { **wishlist.as_dict(), **{ "wishlist_items": list(map(lambda wi: wi.as_dict(), wishlist_items)) } }
    
    return jsonify(wishlist_merged)

@wishlists.route('/get_link_share/<share_guid>')
def get_link_share(share_guid):
    if share_guid is None or len(share_guid) != 8:
        return jsonify({})
    
    wishlist = Wishlist.get_link_share(share_guid)
    
    if wishlist is None:
        return "Not found", 404
    
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
@wishlists.route('/get_count_for_user')
def get_count_for_user():
    count = Wishlist.get_count_for_user(current_user.id)
    
    return jsonify({ "total_wishlists": count })

@login_required
@wishlists.route('/get_shared_with_user')
def get_shared_with_user():
    wishlists = WishlistShare.get_shared_with_user(current_user.id)
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
            order_number=wishlist_item.order_number,
            is_header=wishlist_item.is_header)
    
    return jsonify(id=wishlist_id)

@login_required
@wishlists.route('/update-name/<wishlist_id>', methods=["PATCH"])
def update_name(wishlist_id):
    request_json = json.loads(request.data)
    new_name = request_json['name']
    wishlist = Wishlist.get(wishlist_id, current_user.id)
    
    if wishlist is None:
        return "Not found", 404
    
    wishlist.name = new_name
    wishlist.apply_changes()
    
    return jsonify({})

@login_required
@wishlists.route('/share', methods=["PATCH"])
def share_wishlist():
    request_json = json.loads(request.data)
    
    wishlist = Wishlist.get(request_json['wishlist_id'], current_user.id)
    target_user = User.get_by_email(request_json['email'])

    if not wishlist or not target_user:
        return jsonify({}) # don't expose if a user doesn't exist
    
    UserSharedWishlist.create(user_id=target_user.id, wishlist_id=wishlist.id)
    Wishlist.set_shared(wishlist_id=wishlist.id)
    
    user = User.get(current_user.id)
    
    notify_wishlist_shared(user, target_user, wishlist)
    
    return jsonify({})

@login_required
@wishlists.route('/share-link/<wishlist_id>', methods=["PATCH"])
def share_wishlist_link(wishlist_id: int):
    wishlist = Wishlist.get(wishlist_id, current_user.id)
    
    if not wishlist.share_guid:
        wishlist.share_guid = Wishlist.set_share_guid(wishlist_id)
        
    return jsonify({
        "share_guid": wishlist.share_guid
    })

@login_required
@wishlists.route('/delete/<wishlist_id>', methods=["DELETE"])
def delete(wishlist_id):
    wishlist = Wishlist.get(wishlist_id=wishlist_id, user_id=current_user.id)
    
    if wishlist is None:
        return "Not found", 404
    
    WishlistItem.remove_all_for_wishlist(wishlist_id=wishlist_id)
    Wishlist.remove(wishlist_id=wishlist_id)
    
    return jsonify({})
