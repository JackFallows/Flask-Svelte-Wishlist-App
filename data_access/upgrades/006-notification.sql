CREATE TABLE notification (
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    shared_wishlist_id INT NULL,
    is_read BIT NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (shared_wishlist_id) REFERENCES wishlist(rowid)
)
