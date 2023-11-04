from typing import List
from datetime import datetime
from data_access.models.user import User
from data_access.models.user_shared_wishlist import UserSharedWishlist
from data_access.models.wishlist import Wishlist
from data_access.models.wishlist_item import WishlistItem
from data_access.models.notification import Notification
from services.email_service import send_share_email, send_update_email, send_owner_bought_email
from enums.notification_type import NotificationType

def notify_wishlist_shared(source_user: User, target_user: User, wishlist: Wishlist):
    subject = f"{source_user.name} shared a wishlist with you!"
    message = f"{source_user.name} ({source_user.email}) shared the wishlist '{wishlist.name}' with you."
    
    Notification.create(
        target_user.id,
        message,
        wishlist.id,
        NotificationType.SHARE
    )
    
    if target_user.email_on_share:
        send_share_email(subject, message).to(target_user.email)
    
def notify_wishlist_updated(source_user: User, wishlist: Wishlist):
    if not wishlist.shared:
        return
    
    target_users = UserSharedWishlist.get_users_with_share(wishlist.id)
    
    users_to_email: List[User] = []
    
    def get_can_notify_user(target_user: User) -> bool:
        last_notification = Notification.get_last_wishlist_notification(target_user.id, wishlist.id)
        
        if last_notification is None:
            return True
        
        date_and_time = datetime.fromtimestamp(last_notification.created_at)
        date = date_and_time.date()
        return date < datetime.today().date()
    
    def get_user_notification_message(target_user: User) -> (str, str):
        owner_anonymous = UserSharedWishlist.get_share_is_anonymous(wishlist.id, target_user.id)
        
        if owner_anonymous:
            return (
                f"Items were added to the wishlist '{wishlist.name}'",
                f"Items were added to the wishlist '{wishlist.name}'."
            )
            
        return (
            f"{source_user.name} added items to their wishlist",
            f"{source_user.name} ({source_user.email}) added items to the wishlist '{wishlist.name}'."
        )
    
    for target_user in target_users:
        if not get_can_notify_user(target_user):
            continue
        
        if target_user.email_on_update:
            users_to_email.append(target_user)
            
        (subject, message) = get_user_notification_message(target_user)
            
        Notification.create(
            target_user.id,
            message,
            wishlist.id,
            NotificationType.UPDATE
        )
        
    if len(users_to_email) > 0:
        send_update_email(subject, message).to(list(map(lambda u: u.email, users_to_email)))
        
def notify_owner_bought_item(source_user: User, target_user: User, wishlist: Wishlist, wishlist_item: WishlistItem):
    
    def get_notification_message() -> (str, str):
        owner_anonymous = UserSharedWishlist.get_share_is_anonymous(wishlist.id, target_user.id)
        
        if owner_anonymous:
            return (
                f"An item you bought may have just been bought by the wishlist owner",
                f"The item '{wishlist_item.link}' from the list '{wishlist.name}' may have just been bought by the owner of the wishlist. We're letting you know because you previously marked this item as bought yourself."
            )
        
        return (
            f"{source_user.name} may have just bought an item you already bought",
            f"{source_user.name} ({source_user.email}) may have just bought the item '{wishlist_item.link}' from the list '{wishlist.name}' that they shared with you. We're letting you know because you previously marked this item as bought yourself."
        )
    
    (subject, message) = get_notification_message()
    
    Notification.create(
        target_user.id,
        message,
        wishlist.id,
        NotificationType.OWNER_BOUGHT
    )
    
    if target_user.email_on_owner_bought:
        send_owner_bought_email(subject, message).to(target_user.email)
