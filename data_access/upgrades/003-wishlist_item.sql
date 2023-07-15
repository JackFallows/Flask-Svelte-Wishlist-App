CREATE TABLE wishlist_item (
    wishlist_id INTEGER NOT NULL,
    link TEXT NOT NULL,
    notes TEXT NULL,
    is_bought BIT NOT NULL,
    FOREIGN KEY(wishlist_id) REFERENCES wishlist(rowid)
)
