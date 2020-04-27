import sqlite3 as lite
from threading import Lock

DATABASE_PATH = 'server\\data\\database.db'

class Database(object):
    def __init__(self):
        self.connection = lite.connect(DATABASE_PATH)
        self.lock = Lock()

    def close(self):
        self.connection.close()

    def execute(self, *args):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(*args)
            self.connection.commit()

    def fetch(self, *args):
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute(*args)
            return cursor.fetchall()

database = Database()