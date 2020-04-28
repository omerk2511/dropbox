import sqlite3 as lite
from threading import Lock

DATABASE_PATH = 'server\\data\\database.db'

class Database(object):
    def __init__(self):
        self.lock = Lock()

    def execute(self, *args):
        with self.lock, lite.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(*args)
            connection.commit()

    def fetch(self, *args):
        with self.lock, lite.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(*args)
            return cursor.fetchall()

database = Database()