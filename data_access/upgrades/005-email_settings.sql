ALTER TABLE user
    ADD email_on_share BIT DEFAULT 0;

ALTER TABLE user
    ADD email_on_update BIT DEFAULT 0;
