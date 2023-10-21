from typing import List
from data_access.models.user import User
from data_access.models.wishlist import Wishlist
from data_access.models.notification import Notification
from services.email_service import send_share_email, send_update_email
from enums.notification_type import NotificationType

def notify_wishlist_shared(source_user: User, target_user: User, wishlist: Wishlist):
    Notification.create(
        target_user.id,
        f"{source_user.name} ({source_user.email}) shared the wishlist '{wishlist.name}' with you",
        wishlist.id,
        NotificationType.SHARE
    )
    
    if target_user.email_on_share:
        send_share_email(target_user.email, source_user.name, source_user.email, wishlist.name)
    
def notify_wishlist_updated(source_user: User, target_users: List[User], wishlist: Wishlist):
    users_to_email: List[User] = []
    
    for target_user in target_users:
        if target_user.email_on_update:
            users_to_email.append(target_user)
            
        Notification.create(
            target_user.id,
            f"{source_user.name} ({source_user.email}) updated the wishlist '{wishlist.name}'",
            None,
            NotificationType.UPDATE
        )
        
    if len(users_to_email) > 0:
        send_update_email(list(map(lambda u: u.email, users_to_email)), source_user.name, source_user.email, wishlist.name)
