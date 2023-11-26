ALTER TABLE bought_item
    ADD bought_date DATETIME NULL;

UPDATE bought_item SET bought_date = unixepoch('now');
