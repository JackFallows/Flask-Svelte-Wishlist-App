class NotificationDto():
    def __init__(self, id: int, message: str, created_at: int, shared_wishlist_id: int):
        self.id = id
        self.message = message
        self.created_at = created_at
        self.shared_wishlist_id = shared_wishlist_id
        
    def as_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "created_at": self.created_at,
            "shared_wishlist_id": self.shared_wishlist_id
        } 
