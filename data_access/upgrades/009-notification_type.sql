ALTER TABLE notification
    ADD type INT NULL;

UPDATE notification
    SET type = CASE WHEN shared_wishlist_id IS NULL THEN 1 ELSE 2 END;
