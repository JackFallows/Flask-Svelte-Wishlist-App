CREATE TABLE wishlist (
    name TEXT UNIQUE NOT NULL,
    user_id TEXT NOT NULL,
    shared BIT NOT NULL, -- allows share status to be overridden by the wishlist owner
    deleted BIT NOT NULL
);