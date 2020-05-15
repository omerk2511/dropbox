from initialization import initializer
from ..handlers.database import database

MAX_LOGS = 100

class Logs(object):
    @staticmethod
    @initializer
    def initialize():
        database.execute(
            '''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type CHAR(255) NOT NULL,
                message CHAR(255) NOT NULL
            )
            '''
        )

    @staticmethod
    def get():
        return database.fetch(
            'SELECT * FROM logs',
            ()
        )

    @staticmethod
    def create(log_type, message):
        current_logs = Logs.get()

        if len(current_logs) == MAX_LOGS:
            Logs.delete(current_logs[0][0])

        database.execute(
            'INSERT INTO logs (type, message) VALUES (?, ?)',
            (log_type, message)
        )

    @staticmethod
    def delete(log_id):
        database.execute(
            'DELETE FROM logs WHERE id = ?',
            (log_id,)
        )