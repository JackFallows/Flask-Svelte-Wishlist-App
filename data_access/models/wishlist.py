from flask import jsonify
from data_access.db_connect import get_db_connection

class Wishlist():
    def __init__(self, id, user_id, name, shared, deleted):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.shared = shared
        self.deleted = deleted

    def apply_changes(self):
        if (self.id == None):
            return
        
        db = get_db_connection()
        
        db.execute(
            "UPDATE wishlist SET name = ?, shared = ?, deleted = ? WHERE rowid = ?",
            (self.name, self.shared, self.deleted, self.id,)
        )
        
        db.commit()
        
    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "shared": self.shared,
            "deleted": self.deleted
        }

    @staticmethod
    def get(wishlist_id, user_id):
        db = get_db_connection()
        
        wishlist = db.execute(
            "SELECT rowid, user_id, name, shared, deleted FROM wishlist WHERE rowid = ? AND user_id = ?", (wishlist_id, user_id,)
        ).fetchone()
        
        if not wishlist:
            return None
        
        wishlist = Wishlist(
            id = wishlist[0],
            user_id=wishlist[1],
            name=wishlist[2],
            shared=wishlist[3],
            deleted=wishlist[4]
        )
        
        return jsonify(wishlist.as_dict())
    
    @staticmethod
    def get_all_for_user(user_id):
        db = get_db_connection()
        
        wishlists = db.execute(
            "SELECT * FROM wishlist WHERE user_id = ?", (user_id,)
        ).fetchall()
        
        return list(map(lambda w: Wishlist(id=w[0], user_id=w[1], name=w[2], shared=w[3], deleted=w[4]), wishlists))
    
    @staticmethod
    def create(name, user_id):
        with get_db_connection() as db:
            db.execute(
                "INSERT INTO wishlist (user_id, name, shared, deleted) "
                "VALUES (?, ?, 0, 0)",
                (user_id, name,),
            )
            
            db.commit()
            
            wishlist_id = db.execute(
                "SELECT rowid FROM wishlist WHERE name = ?",
                (name,)
            ).fetchone()[0]
            
            return wishlist_id
        