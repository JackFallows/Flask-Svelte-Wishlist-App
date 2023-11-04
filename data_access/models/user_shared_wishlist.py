from typing import List
from data_access.db_connect import get_db_connection
from data_access.models.user import User

class UserSharedWishlist():
    def __init__(self, id, user_id, wishlist_id, accepted, owner_anonymous):
        self.id = id
        self.user_id = user_id
        self.wishlist_id = wishlist_id
        self.accepted = accepted
        self.owner_anonymous = owner_anonymous
        
    @staticmethod
    def get(share_id):
        with get_db_connection() as db:
            usw = db.execute(
                "SELECT rowid, user_id, wishlist_id, accepted, owner_anonymous "
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
                accepted=usw[3],
                owner_anonymous=usw[4]
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
    def create(user_id, wishlist_id, owner_anonymous=False):
        with get_db_connection() as db:
            
            # ensure has not already been shared with user
            existing = db.execute(
                """
                SELECT rowid FROM user_shared_wishlist WHERE user_id = ? AND wishlist_id = ?
                """,
                (user_id, wishlist_id,)
            ).fetchone()
            
            if existing is not None:
                return
            
            # ensure owner is not trying to share with themself
            owner = db.execute(
                """
                SELECT user_id FROM wishlist WHERE user_id = ? AND rowid = ?
                """,
                (user_id, wishlist_id,)
            ).fetchone()
            
            if owner is not None:
                return
            
            db.execute(
                "INSERT INTO user_shared_wishlist (user_id, wishlist_id, accepted, owner_anonymous) "
                "VALUES (?, ?, ?, ?)",
                (user_id, wishlist_id, 1 if owner_anonymous == True else None, owner_anonymous,)
            )
            
            db.commit()
        
    @staticmethod
    def get_users_with_share(wishlist_id: int) -> List[User]:
        with get_db_connection() as db:
            users = db.execute("""
                SELECT id, name, email, profile_pic, internal_password, email_on_share, email_on_update, email_on_owner_bought
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
                email_on_update=user[6],
                email_on_owner_bought=user[7]
            ), users))
            
    @staticmethod
    def get_existing(wishlist_id: int, user_id: str):
        with get_db_connection() as db:
            usw = db.execute(
                """
                SELECT rowid, user_id, wishlist_id, accepted, owner_anonymous 
                FROM user_shared_wishlist 
                WHERE wishlist_id = ? AND user_id = ?
                """,
                (wishlist_id, user_id,)
            ).fetchone()
            
            if not usw:
                return None
            
            return UserSharedWishlist(
                id=usw[0],
                user_id=usw[1],
                wishlist_id=usw[2],
                accepted=usw[3],
                owner_anonymous=usw[4]
            )
            
    @staticmethod
    def get_share_is_anonymous(wishlist_id: int, user_id: str) -> bool:
        with get_db_connection() as db:
            owner_anonymous = db.execute(
                """
                SELECT owner_anonymous FROM user_shared_wishlist usw WHERE user_id = ? AND wishlist_id = ?
                """,
                (user_id, wishlist_id,)
            ).fetchone()
            
            return True if owner_anonymous[0] == 1 else False
        
    @staticmethod
    def set_not_anonymous(share_id: int):
        with get_db_connection() as db:
            db.execute(
                """
                UPDATE user_shared_wishlist SET owner_anonymous = 0 WHERE rowid = ?
                """,
                (share_id,)
            )
            
            db.commit()
            
    @staticmethod
    def remove_all_for_wishlist(wishlist_id: int):
        with get_db_connection() as db:
            db.execute(
                """
                DELETE FROM user_shared_wishlist WHERE wishlist_id = ?
                """,
                (wishlist_id,)
            )
            
            db.commit()
