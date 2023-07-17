CREATE TABLE user_shared_wishlist (
    user_id TEXT NOT NULL, -- user with whom the wishlist has been shared
    wishlist_id INTEGER NOT NULL,
    accepted BIT NULL, -- whether the target user has accepted the share request (NULL until they respond, 0 if rejected (so they can't be spammed), 1 if accepted)
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (wishlist_id) REFERENCES wishlist(rowid)
)
