import sqlite3
from os import listdir
import os

from flask import current_app, g
from flask.cli import with_appcontext

from data_access.db_connect import get_db_connection
from data_access.models.schema_version import SchemaVersion

def get_db():
    if "db" not in g:
        g.db = get_db_connection()

        try:
            g.db.execute("SELECT * FROM schema_version").fetchall()
        except sqlite3.OperationalError:
            # schema_version table probably doesn't exist - create it
            with current_app.open_resource("data_access/base.sql") as f:
                g.db.executescript(f.read().decode("utf8"))

            # then add the current script to the table
            SchemaVersion.create(filename="base.sql")

    return g.db

def close_db(e=None):
    db = g.pop("db", None);

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    upgrade_files = listdir("data_access/upgrades")
    upgrade_files.sort()

    executed_files = SchemaVersion.get_all()

    for upgrade_file in upgrade_files:
        if upgrade_file in executed_files:
            continue

        with current_app.open_resource(os.path.join("data_access/upgrades", upgrade_file)) as f:
            db.executescript(f.read().decode("utf8"))
        
        SchemaVersion.create(filename=upgrade_file)

@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
