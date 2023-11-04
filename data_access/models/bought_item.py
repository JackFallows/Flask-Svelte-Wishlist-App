from datetime import datetime
from data_access.db_connect import get_db_connection

class BoughtItem():
    def __init__(self, id, user_id, wishlist_item_id, defer_until):
        self.id = id
        self.user_id = user_id
        self.wishlist_item_id = wishlist_item_id
        self.defer_until = defer_until
        
    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "wishlist_item_id": self.wishlist_item_id,
            "defer_until": self.defer_until
        }
        
    @staticmethod
    def create(user_id: str, wishlist_item_id: int, defer_until: str):
        defer_until_time = None
        
        if defer_until is not None:
            defer_until_time = datetime.strptime(defer_until, "%Y-%m-%d").timestamp()
        
        with get_db_connection() as db:
            db.execute(
                """
                INSERT INTO bought_item (user_id, wishlist_item_id, defer_until)
                VALUES (?, ?, ?)
                """,
                (user_id, wishlist_item_id, defer_until_time,)
            )
            
            db.commit()
            
            bought_item_id = db.execute(
                "SELECT last_insert_rowid()"
            ).fetchone()[0]
            
            return BoughtItem(
                id=bought_item_id,
                user_id=user_id,
                wishlist_item_id=int(wishlist_item_id),
                defer_until=defer_until_time
            )
            
    @staticmethod
    def remove_defer_date(id: int, user_id: str):
        with get_db_connection() as db:
            db.execute(
                """
                UPDATE bought_item SET defer_until = NULL, user_id = ? WHERE rowid = ?
                """,
                (user_id, id,)
            )
            
            db.commit()
            
    @staticmethod
    def get_for_wishlist(wishlist_id: int):
        with get_db_connection() as db:
            bought_items_result = db.execute(
                """
                SELECT bi.rowid, bi.user_id, bi.wishlist_item_id, bi.defer_until
                FROM bought_item bi
                JOIN wishlist_item wi ON wi.rowid = bi.wishlist_item_id
                WHERE wi.wishlist_id = ?
                """,
                (wishlist_id,)
            ).fetchall()
            
            return list(
                map(
                    lambda bi: BoughtItem(
                        id=bi[0],
                        user_id=bi[1],
                        wishlist_item_id=bi[2],
                        defer_until=bi[3]),
                    bought_items_result)
                )
            
            
