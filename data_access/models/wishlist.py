import string
import random
from data_access.db_connect import get_db_connection
from api.models.wishlist_link_share import WishlistLinkShare

class Wishlist():
    def __init__(self, id, user_id, name, shared, deleted, share_guid):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.shared = shared
        self.deleted = deleted
        self.share_guid = share_guid
        
    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "shared": self.shared,
            "deleted": self.deleted,
            "share_guid": self.share_guid
        }

    def apply_changes(self):
        if (self.id == None):
            return
        
        with get_db_connection() as db:
            db.execute(
                "UPDATE wishlist SET name = ? WHERE rowid = ?",
                (self.name, self.id,)
            )
            
            db.commit()
            
    @staticmethod
    def from_json(json):
        return Wishlist(
            id=json['id'],
            user_id=json['user_id'],
            name=json['name'],
            shared=json['shared'],
            deleted=json['deleted'],
            share_guid=json['share_guid']
        )

    @staticmethod
    def get(wishlist_id, user_id):
        with get_db_connection() as db:
            wishlist = db.execute(
                "SELECT rowid, user_id, name, shared, deleted, share_guid FROM wishlist WHERE rowid = ? AND user_id = ?", (wishlist_id, user_id,)
            ).fetchone()
            
            if not wishlist:
                return None
            
            wishlist = Wishlist(
                id = wishlist[0],
                user_id=wishlist[1],
                name=wishlist[2],
                shared=wishlist[3],
                deleted=wishlist[4],
                share_guid=wishlist[5]
            )
            
            return wishlist
        
    @staticmethod
    def get_link_share(share_guid):
        with get_db_connection() as db:
            wishlist = db.execute(
                "SELECT rowid, name, share_guid FROM wishlist WHERE share_guid = ?", (share_guid,)
            ).fetchone()
            
            if not wishlist:
                return None
            
            wishlist = WishlistLinkShare(
                id = wishlist[0],
                name = wishlist[1],
                share_guid = wishlist[2]
            )
            
            return wishlist
    
    @staticmethod
    def get_all_for_user(user_id):
        with get_db_connection() as db:
            wishlists = db.execute(
                "SELECT rowid, user_id, name, shared, deleted, share_guid FROM wishlist WHERE user_id = ?", (user_id,)
            ).fetchall()
            
            return list(
                map(
                    lambda w: Wishlist(
                        id=w[0],
                        user_id=w[1],
                        name=w[2],
                        shared=w[3],
                        deleted=w[4],
                        share_guid=w[5]),
                    wishlists)
                )
        
    @staticmethod
    def create(name, user_id):
        with get_db_connection() as db:
            db.execute(
                "INSERT INTO wishlist (user_id, name, shared, deleted, share_guid) "
                "VALUES (?, ?, 0, 0, NULL)",
                (user_id, name,),
            )
            
            db.commit()
            
            wishlist_id = db.execute(
                "SELECT last_insert_rowid()"
            ).fetchone()[0]
            
            return wishlist_id

    @staticmethod
    def set_shared(wishlist_id):
        with get_db_connection() as db:
            db.execute(
                "UPDATE wishlist SET shared = 1 WHERE rowid = ?",
                (wishlist_id,)
            )
            db.commit()
            
    @staticmethod
    def set_share_guid(wishlist_id) -> str:
        with get_db_connection() as db:
            existing = db.execute("SELECT share_guid FROM wishlist WHERE share_guid IS NOT NULL AND rowid != ?", (wishlist_id,)).fetchall()
            unavailable_guids = list(map(lambda x: x[0], existing))
            
            def generate_guid():
                alphabet = string.ascii_lowercase + string.digits
                return ''.join(random.choices(alphabet, k=8))    
            
            share_guid = generate_guid()
                        
            while share_guid in unavailable_guids:
                share_guid = generate_guid()
            
            db.execute(
                "UPDATE wishlist SET share_guid = ? WHERE rowid = ?",
                (share_guid, wishlist_id,)
            )
            
            return share_guid

    @staticmethod
    def remove(wishlist_id):
        with get_db_connection() as db:
            db.execute(
                "DELETE FROM wishlist WHERE rowid = ?",
                (wishlist_id,)
            )
            db.commit()

