from common import Codes, Message
from ..handlers.connection import Connection

class SignUpController(object):
    @staticmethod
    def sign_up(username, full_name, password):
        return Connection.send_recieve(
            Message(
                Codes.SIGN_UP,
                {
                    'username': username,
                    'full_name': full_name,
                    'password': password
                }
            )
        )