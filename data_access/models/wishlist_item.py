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
                "FROM wishlist_item "
                "WHERE wishlist_id = ? AND bought = 0 "
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
    def get_ids_for_wishlist(wishlist_id):
        with get_db_connection() as db:
            ids = db.execute(
                "SELECT rowid FROM wishlist_item WHERE wishlist_id = ?",
                (wishlist_id,)
            ).fetchall()
            
            return list(map(lambda x: x[0], ids))
    
            
    @staticmethod
    def get_is_available_to_user(wishlist_item_id, user_id):
        with get_db_connection() as db:
            wishlist_item = db.execute(
                "SELECT wishlist_item.rowid "
                "FROM wishlist_item "
                "INNER JOIN wishlist ON wishlist.rowid = wishlist_item.wishlist_id "
                "LEFT OUTER JOIN user_shared_wishlist AS usw ON usw.wishlist_id = wishlist.rowid "
                "WHERE wishlist_item.rowid = ? AND (wishlist.user_id = ? OR (usw.user_id = ? AND usw.accepted = 1 AND wishlist.shared = 1))",
                (wishlist_item_id, user_id, user_id,)
            ).fetchone()
            
            if not wishlist_item:
                return False
            
            return True
        
    @staticmethod
    def get_is_owned_by_user(wishlist_item_id, user_id):
        with get_db_connection() as db:
            wishlist_item = db.execute(
                """
                SELECT wi.rowid
                FROM wishlist_item wi
                INNER JOIN wishlist w ON w.rowid = wi.wishlist_id
                WHERE wi.rowid = ? AND w.user_id = ?
                """, (wishlist_item_id, user_id,)
            ).fetchone()
            
            if not wishlist_item:
                return False
            
            return True
        
    @staticmethod
    def get_is_available_to_link_share(wishlist_item_id, share_guid):
        with get_db_connection() as db:
            wishlist_item = db.execute(
                """
                SELECT wishlist_item.rowid
                FROM wishlist_item
                INNER JOIN wishlist ON wishlist.rowid = wishlist_item.wishlist_id
                WHERE wishlist.share_guid = ? AND wishlist_item.rowid = ?
                """, (share_guid, wishlist_item_id,)
            ).fetchone()
            
            if not wishlist_item:
                return False
            
            return True
        
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
        
    @staticmethod
    def set_as_bought(wishlist_item_id):
        with get_db_connection() as db:
            db.execute(
                "UPDATE wishlist_item SET bought = 1 WHERE rowid = ?",
                (wishlist_item_id,)
            )
            db.commit()
            
    @staticmethod
    def reparent(wishlist_item_id: int, wishlist_id: int):
        with get_db_connection() as db:
            db.execute(
                """
                UPDATE wishlist_item SET wishlist_id = ? WHERE rowid = ?
                """, (wishlist_id, wishlist_item_id,)
            )
            
            db.commit()
            
    @staticmethod
    def remove(wishlist_item_id):
        with get_db_connection() as db:
            db.execute(
                "DELETE FROM wishlist_item WHERE rowid = ?",
                (wishlist_item_id,)
            )
            db.commit()
            
    @staticmethod
    def remove_all_for_wishlist(wishlist_id):
        with get_db_connection() as db:
            db.execute(
                "DELETE FROM wishlist_item WHERE wishlist_id = ?",
                (wishlist_id,)
            )
            db.commit()
