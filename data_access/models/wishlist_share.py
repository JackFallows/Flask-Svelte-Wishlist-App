from data_access.db_connect import get_db_connection
from data_access.models.wishlist import Wishlist

class WishlistShare(Wishlist):
    def __init__(self, id, user_id, name, shared, deleted, owner_name, owner_email):
        super().__init__(id, user_id, name, shared, deleted)
        self.owner_name = owner_name
        self.owner_email = owner_email
        
    def as_dict(self):
        dict = super().as_dict()
        
        return {
            **dict,
            **{
                "owner_name": self.owner_name,
                "owner_email": self.owner_email
            }
        }
        
    @staticmethod
    def get(user_id, wishlist_id):
        with get_db_connection() as db:
            wishlist = db.execute(
                "SELECT w.rowid, w.user_id, w.name, w.shared, w.deleted, u.name, u.email "
                "FROM wishlist AS w "
                "INNER JOIN user_shared_wishlist AS usw ON w.rowid = usw.wishlist_id "
                "INNER JOIN user AS u ON u.id = w.user_id "
                "WHERE usw.user_id = ? AND w.rowid = ? AND w.shared = 1 AND usw.accepted = 1 ",
                (user_id, wishlist_id,)
            ).fetchone()
            
            if not wishlist:
                return None
            
            wishlist = WishlistShare(
                id=wishlist[0],
                user_id=wishlist[1],
                name=wishlist[2],
                shared=wishlist[3],
                deleted=wishlist[4],
                owner_name=wishlist[5],
                owner_email=wishlist[6],
            )
            
            return wishlist
        
    @staticmethod
    def get_shared_with_user(user_id):
        with get_db_connection() as db:
            wishlists = db.execute(
                "SELECT w.rowid, w.user_id, w.name, w.shared, w.deleted, u.name, u.email "
                "FROM wishlist AS w "
                "INNER JOIN user_shared_wishlist AS usw ON w.rowid = usw.wishlist_id "
                "INNER JOIN user AS u ON u.id = w.user_id "
                "WHERE usw.user_id = ? AND w.shared = 1 AND usw.accepted = 1 ",
                (user_id,)
            ).fetchall()
            
            return list(
                map(
                    lambda w: WishlistShare(
                        id=w[0],
                        user_id=w[1],
                        name=w[2],
                        shared=w[3],
                        deleted=w[4],
                        owner_name=w[5],
                        owner_email=w[6],
                    ),
                    wishlists
                )
            )