BEGIN TRANSACTION;

CREATE TABLE bought_item (
    user_id TEXT NULL,
    wishlist_item_id INT NOT NULL,
    defer_until DATETIME NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(wishlist_item_id) REFERENCES wishlist_item(rowid)
);

INSERT INTO bought_item (wishlist_item_id)
    SELECT rowid
    FROM wishlist_item
    WHERE bought = 1;

ALTER TABLE wishlist_item
    DROP COLUMN bought;

COMMIT;
