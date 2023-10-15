from typing import List
from data_access.db_connect import get_db_connection
from data_access.models.user import User

class UserSharedWishlist():
    def __init__(self, id, user_id, wishlist_id, accepted):
        self.id = id
        self.user_id = user_id
        self.wishlist_id = wishlist_id
        self.accepted = accepted
        
    @staticmethod
    def get(share_id):
        with get_db_connection() as db:
            usw = db.execute(
                "SELECT rowid, user_id, wishlist_id, accepted "
                "FROM user_shared_wishlist "
                "WHERE rowid = ?",
                (share_id,)
            ).fetchone()
            
            if not usw:
                return None
            
            return UserSharedWishlist(
                id=usw[0],
                user_id=usw[1],
                wishlist_id=usw[2],
                accepted=usw[3]
            )
        
    @staticmethod
    def set_accepted(user_id, wishlist_id, accepted):
        with get_db_connection() as db:
            db.execute(
                "UPDATE user_shared_wishlist SET accepted = ? WHERE user_id = ? AND wishlist_id = ?",
                (accepted, user_id, wishlist_id,)
            )
            db.commit()
        
    @staticmethod
    def create(user_id, wishlist_id):
        with get_db_connection() as db:
            db.execute(
                "INSERT INTO user_shared_wishlist (user_id, wishlist_id, accepted) "
                "VALUES (?, ?, NULL)",
                (user_id, wishlist_id,)
            )
            
            db.commit()
        
    @staticmethod
    def get_users_with_share(wishlist_id: int) -> List[User]:
        with get_db_connection() as db:
            users = db.execute("""
                SELECT id, name, email, profile_pic, internal_password, email_on_share, email_on_update
                FROM user AS u
                INNER JOIN user_shared_wishlist AS usw ON u.id = usw.user_id
                WHERE usw.wishlist_id = ? and usw.accepted = 1
                """,
                (wishlist_id,)
            ).fetchall()
            
            return list(map(lambda user: User(
                id_ = user[0],
                name=user[1],
                email=user[2],
                profile_pic=user[3],
                internal_password=user[4],
                email_on_share=user[5],
                email_on_update=user[6]
            ), users))
