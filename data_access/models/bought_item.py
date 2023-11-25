from datetime import datetime, date
from data_access.db_connect import get_db_connection

class BoughtItem():
    def __init__(self, id, user_id, wishlist_item_id, defer_until, bought_date):
        self.id = id
        self.user_id = user_id
        self.wishlist_item_id = wishlist_item_id
        self.defer_until = defer_until
        self.bought_date = bought_date
        
    def as_dict(self, current_user_id: str):
        return {
            "id": self.id,
            "current_user_bought": self.user_id == current_user_id,
            "wishlist_item_id": self.wishlist_item_id,
            "defer_until": self.defer_until,
            "bought_date": self.bought_date
        }
        
    @staticmethod
    def create(user_id: str, wishlist_item_id: int, defer_until: str):
        defer_until_time = None
        
        if defer_until is not None:
            defer_until_time = datetime.strptime(defer_until, "%Y-%m-%d").timestamp()
            
        now = datetime.now()
        timestamp = int(now.timestamp())
        
        with get_db_connection() as db:
            db.execute(
                """
                INSERT INTO bought_item (user_id, wishlist_item_id, defer_until, bought_date)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, wishlist_item_id, defer_until_time, timestamp,)
            )
            
            db.commit()
            
            bought_item_id = db.execute(
                "SELECT last_insert_rowid()"
            ).fetchone()[0]
            
            return BoughtItem(
                id=bought_item_id,
                user_id=user_id,
                wishlist_item_id=int(wishlist_item_id),
                defer_until=defer_until_time,
                bought_date=timestamp
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
                SELECT bi.rowid, bi.user_id, bi.wishlist_item_id, bi.defer_until, bi.bought_date
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
                        defer_until=bi[3],
                        bought_date=bi[4]),
                    bought_items_result)
                )
            
    @staticmethod
    def get_for_wishlist_owner(wishlist_id: int, user_id: str):
        with get_db_connection() as db:
            today = datetime.combine(date.today(), datetime.min.time()).timestamp()
            
            bought_items_result = db.execute(
                """
                SELECT bi.rowid, bi.user_id, bi.wishlist_item_id, bi.defer_until, bi.bought_date
                FROM bought_item bi
                JOIN wishlist_item wi ON wi.rowid = bi.wishlist_item_id
                WHERE wi.wishlist_id = ? AND (bi.user_id = ? OR bi.defer_until IS NULL OR bi.defer_until < ?)
                """,
                (wishlist_id, user_id, today,)
            ).fetchall()
            
            return list(
                map(
                    lambda bi: BoughtItem(
                        id=bi[0],
                        user_id=bi[1],
                        wishlist_item_id=bi[2],
                        defer_until=bi[3],
                        bought_date=bi[4]),
                    bought_items_result)
                )
            
            
