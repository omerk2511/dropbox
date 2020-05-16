from common import Codes, Message
from ..handlers.connection import Connection

class SignUpController(object):
    @staticmethod
    def sign_up(username, full_name, password):
        """
        Signs a user up
        args: username, full_name, password
        ret: response
        """

        return Connection().send_recieve(
            Message(
                Codes.CREATE_USER,
                {
                    'username': username,
                    'full_name': full_name,
                    'password': password
                }
            )
        )