import sqlite3

def get_db_connection():
    db = sqlite3.connect(
        "sqlite_db", detect_types=sqlite3.PARSE_DECLTYPES
    )

    db.row_factory = sqlite3.Row

    return db