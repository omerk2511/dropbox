from common import Codes, Message
from ..handlers.connection import Connection

class LogInController(object):
    @staticmethod
    def log_in(username, password):
        return Connection().send_recieve(
            Message(
                Codes.LOG_IN,
                {
                    'username': username,
                    'password': password
                }
            )
        )