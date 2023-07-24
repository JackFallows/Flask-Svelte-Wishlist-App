import os
import sqlite3

SQLITE_DB = os.environ.get("SQLITE_DB", "sqlite_db.db")

def get_db_connection():
    db = sqlite3.connect(
        SQLITE_DB, detect_types=sqlite3.PARSE_DECLTYPES
    )

    db.row_factory = sqlite3.Row

    return db
