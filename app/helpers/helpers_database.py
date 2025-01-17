# Python Standard Library
import sqlite3










class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        return self.cursor
        
    def __exit__(self, exception_type, exception_value, exception_traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.commit()
            self.connection.close()
