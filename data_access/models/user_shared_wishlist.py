from data_access.db_connect import get_db_connection

class UserSharedWishlist():
    def __init__(self, id, user_id, wishlist_id, accepted):
        self.id = id
        self.user_id = user_id
        self.wishlist_id = wishlist_id
        self.accepted = accepted
        
    @staticmethod
    def get_pending_shares(user_id):
        with get_db_connection() as db:
            pending = db.execute(
                "SELECT u.name AS user_name, u.email, usw.wishlist_id, w.name AS wishlist_name "
                "FROM user_shared_wishlist AS usw "
                "INNER JOIN wishlist AS w ON w.rowid = usw.wishlist_id "
                "INNER JOIN user AS u ON u.id = w.user_id "
                "WHERE usw.accepted IS NULL AND usw.user_id = ?",
                (user_id,)
            ).fetchall()
            
            return list(
                map(
                    lambda usw: {
                        "user_name": usw[0],
                        "email": usw[1],
                        "wishlist_id": usw[2],
                        "wishlist_name": usw[3]
                    },
                    pending
                )
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
