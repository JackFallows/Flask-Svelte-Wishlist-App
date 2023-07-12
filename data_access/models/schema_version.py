from data_access.db_connect import get_db_connection

class SchemaVersion():
    def __init__(self, rowid, filename):
        self.rowid = rowid
        self.filename = filename
    
    @staticmethod
    def get_all():
        db = get_db_connection()
        schema_versions = db.execute(
            "SELECT filename FROM schema_version"
        ).fetchall()

        # map the results to a list of just the filenames
        return list(map(lambda r: r[0], schema_versions))
    
    @staticmethod
    def create(filename):
        db = get_db_connection()
        db.execute(
            "INSERT INTO schema_version (filename) "
            "VALUES (?)",
            (filename,), # trailing comma inside the parentheses to make it a tuple
        )
        db.commit()