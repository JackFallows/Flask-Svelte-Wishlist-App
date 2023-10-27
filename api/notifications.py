from typing import List
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from data_access.models.user_shared_wishlist import UserSharedWishlist
from data_access.models.notification import Notification
from api.models.notification_dto import NotificationDto

notifications = Blueprint('notifications', __name__)

@notifications.route('/get')
@login_required
def get():
    notifications = Notification.get_all_for_user(current_user.id)
    
    notification_dtos: List[NotificationDto] = []
    
    for notification in notifications:
        notification_dtos.append(NotificationDto(
            notification.id,
            notification.message,
            notification.created_at,
            notification.shared_wishlist_id,
            notification.type
        ))
    
    return jsonify(list(map(lambda x: x.as_dict(), notification_dtos)))

@notifications.route('/read/<notification_id>', methods=["PATCH"])
@login_required
def read(notification_id):
    notification = Notification.get(notification_id)
    
    notification.is_read = 1
    notification.apply_changes()
    
    return jsonify({})

@notifications.route('/accept_share/<notification_id>', methods=["PATCH"])
@login_required
def accept_share(notification_id):
    notification = Notification.get(notification_id)
    
    UserSharedWishlist.set_accepted(user_id=current_user.id, wishlist_id=notification.shared_wishlist_id, accepted=True)
    
    notification.is_read = 1
    notification.apply_changes()
    
    return jsonify({})
    
@notifications.route('/reject_share/<notification_id>', methods=["PATCH"])
@login_required
def reject_share(notification_id):
    notification = Notification.get(notification_id)
    
    UserSharedWishlist.set_accepted(user_id=current_user.id, wishlist_id=notification.shared_wishlist_id, accepted=False)
    
    notification.is_read = 1
    notification.apply_changes()
    
    return jsonify({})
