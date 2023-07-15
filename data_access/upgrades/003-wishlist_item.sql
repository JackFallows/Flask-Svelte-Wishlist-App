CREATE TABLE wishlist_item (
    wishlist_id INTEGER NOT NULL,
    link TEXT NOT NULL,
    notes TEXT NULL,
    bought BIT NOT NULL,
    order_number INTEGER NOT NULL,
    FOREIGN KEY(wishlist_id) REFERENCES wishlist(rowid)
)
