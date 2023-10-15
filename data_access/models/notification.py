import datetime

from data_access.db_connect import get_db_connection

class Notification():
    def __init__(self, id, user_id, message, created_at, shared_wishlist_id, is_read):
        self.id = id
        self.user_id = user_id
        self.message = message
        self.created_at = created_at
        self.shared_wishlist_id = shared_wishlist_id
        self.is_read = is_read

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "created_at": self.created_at,
            "shared_wishlist_id": self.shared_wishlist_id,
            "is_read": self.is_read
        }     
        
    @staticmethod
    def create(user_id, message, shared_wishlist_id):
        now = datetime.datetime.now()
        timestamp = int(now.timestamp())
        
        with get_db_connection() as db:
            db.execute(
                "INSERT INTO notification (user_id, message, created_at, shared_wishlist_id, is_read) "
                "VALUES (?, ?, ?, ?, 0)",
                (user_id, message, timestamp, shared_wishlist_id,),
            )
            
            db.commit()
            
    def apply_changes(self):
        if (self.id == None):
            return
        
        with get_db_connection() as db:
            db.execute(
                "UPDATE notification SET is_read = ? WHERE rowid = ?",
                (self.is_read, self.id,)
            )
            
            db.commit()
            
    @staticmethod
    def get(notification_id):
        with get_db_connection() as db:
            notification = db.execute("""
                SELECT rowid, user_id, message, created_at, shared_wishlist_id, is_read
                FROM notification
                WHERE rowid = ? AND is_read = 0
            """, (notification_id,)
            ).fetchone()
            
            if not notification:
                return None
            
            return Notification(
                id=notification[0],
                user_id=notification[1],
                message=notification[2],
                created_at=notification[3],
                shared_wishlist_id=notification[4],
                is_read=notification[5])
        
    @staticmethod
    def get_all_for_user(user_id):
        with get_db_connection() as db:
            notifications = db.execute("""
                SELECT rowid, user_id, message, created_at, shared_wishlist_id, is_read
                FROM notification
                WHERE user_id = ? AND is_read = 0
                ORDER BY created_at DESC
            """, (user_id,)
            ).fetchall()
            
            return list(
                map(
                    lambda n: Notification(
                        id=n[0],
                        user_id=n[1],
                        message=n[2],
                        created_at=n[3],
                        shared_wishlist_id=n[4],
                        is_read=n[5]),
                    notifications)
                )
