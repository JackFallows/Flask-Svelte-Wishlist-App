class WishlistLinkShare():
    def __init__(self, id, name, share_guid):
        self.id = id
        self.name = name
        self.share_guid = share_guid
        
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "share_guid": self.share_guid
        }
