import sqlite3 as lite
from threading import Lock

from ..config import DATABASE_PATH

class Database(object):
    def __init__(self):
        """
        Creates a Database object
        args: self
        ret: none
        """

        self.lock = Lock()

    def execute(self, *args):
        """
        Executes a database query
        args: self, *args
        ret: last_row_id
        """

        with self.lock, lite.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(*args)
            connection.commit()
            return cursor.lastrowid

    def fetch(self, *args):
        """
        Executes a database query and returns the results
        args: self, *args
        ret: results
        """

        with self.lock, lite.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(*args)
            return cursor.fetchall()

database = Database()