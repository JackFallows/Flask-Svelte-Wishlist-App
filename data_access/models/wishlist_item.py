from data_access.db_connect import get_db_connection

class WishlistItem():
    def __init__(self, id, wishlist_id, link, notes, is_bought):
        self.id = id
        self.wishlist_id = wishlist_id
        self.link = link
        self.notes = notes
        self.is_bought = is_bought
        
    def as_dict(self):
        return {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "link": self.link,
            "notes": self.notes,
            "is_bought": self.is_bought
        }
        
    def apply_changes(self):
        if (self.id == None):
            return
        
        with get_db_connection() as db:
            db.execute(
                "UPDATE wishlist_item SET link = ?, notes = ?, is_bought = ? WHERE rowid = ?",
                (self.link, self.notes, self.is_bought, self.id,)
            )
            
            db.commit()
        
    @staticmethod
    def get_all_for_wishlist(wishlist_id):
        with get_db_connection() as db:
            wishlist_items = db.execute(
                "SELECT rowid, wishlist_id, link, notes, is_bought FROM wishlist_item WHERE wishlist_id = ?", (wishlist_id,)
            ).fetchall()
            
            return list(
                map(
                    lambda w: WishlistItem(
                        id=w[0],
                        wishlist_id=w[1],
                        link=w[2],
                        notes=w[3],
                        is_bought=w[4]),
                    wishlist_items)
                )
        
    @staticmethod
    def create(wishlist_id, link, notes):
        with get_db_connection() as db:
            db.execute(
                "INSERT INTO wishlist_item (wishlist_id, link, notes, is_bought) "
                "VALUES (?, ?, ?, 0)",
                (wishlist_id, link, notes,),
            )
            
            db.commit()
            
            wishlist_item_id = db.execute(
                "SELECT last_insert_rowid()"
            ).fetchone()[0]
            
            return wishlist_item_id
