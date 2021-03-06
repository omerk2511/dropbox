from initialization import initializer
from ..handlers.database import database

MAX_LOGS = 100

class Logs(object):
    @staticmethod
    @initializer
    def initialize():
        """
        Initializes the logs table
        args: none
        ret: none
        """

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
        """
        Gets all the logs
        args: none
        ret: logs
        """

        return database.fetch(
            'SELECT * FROM logs',
            ()
        )

    @staticmethod
    def create(log_type, message):
        """
        Creates a log
        args: log_type, message
        ret: none
        """

        current_logs = Logs.get()

        error_logs = [log for log in current_logs if log[1] == 'error']
        activity_logs = [log for log in current_logs if log[1] == 'activity']

        if log_type == 'error' and len(error_logs) == MAX_LOGS:
            Logs.delete(error_logs[0][0])
        
        if log_type == 'activity' and len(activity_logs) == MAX_LOGS:
            Logs.delete(activity_logs[0][0])

        database.execute(
            'INSERT INTO logs (type, message) VALUES (?, ?)',
            (log_type, message)
        )

    @staticmethod
    def delete(log_id):
        """
        Deletes a log
        args: log_id
        ret: none
        """

        database.execute(
            'DELETE FROM logs WHERE id = ?',
            (log_id,)
        )