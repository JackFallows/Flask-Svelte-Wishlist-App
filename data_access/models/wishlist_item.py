from data_access.db_connect import get_db_connection

class WishlistItem():
    def __init__(self, id, wishlist_id, link, notes, bought, order_number):
        self.id = id
        self.wishlist_id = wishlist_id
        self.link = link
        self.notes = notes
        self.bought = bought
        self.order_number = order_number
        
    def as_dict(self):
        return {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "link": self.link,
            "notes": self.notes,
            "bought": self.bought,
            "order_number": self.order_number
        }
        
    def apply_changes(self):
        if (self.id == None):
            return
        
        with get_db_connection() as db:
            db.execute(
                "UPDATE wishlist_item SET link = ?, notes = ?, bought = ?, order_number = ? WHERE rowid = ?",
                (self.link, self.notes, self.bought, self.order_number, self.id,)
            )
            
            db.commit()
        
    @staticmethod
    def from_json(json):
        return WishlistItem(
            id=json['id'],
            wishlist_id=json['wishlist_id'],
            link=json['link'],
            notes=json['notes'],
            bought=json['bought'],
            order_number=json['order_number']
        )
        
    @staticmethod
    def get_all_for_wishlist(wishlist_id):
        with get_db_connection() as db:
            wishlist_items = db.execute(
                "SELECT rowid, wishlist_id, link, notes, bought, order_number "
                "FROM wishlist_item WHERE wishlist_id = ? "
                "ORDER BY order_number", (wishlist_id,)
            ).fetchall()
            
            return list(
                map(
                    lambda w: WishlistItem(
                        id=w[0],
                        wishlist_id=w[1],
                        link=w[2],
                        notes=w[3],
                        bought=w[4],
                        order_number=w[5]),
                    wishlist_items)
                )
        
    @staticmethod
    def create(wishlist_id, link, notes, order_number):
        with get_db_connection() as db:
            db.execute(
                "INSERT INTO wishlist_item (wishlist_id, link, notes, bought, order_number) "
                "VALUES (?, ?, ?, 0, ?)",
                (wishlist_id, link, notes, order_number,),
            )
            
            db.commit()
            
            wishlist_item_id = db.execute(
                "SELECT last_insert_rowid()"
            ).fetchone()[0]
            
            return wishlist_item_id
