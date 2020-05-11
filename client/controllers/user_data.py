from common import Codes, Message
from ..handlers.connection import Connection

class UserDataController(object):
    @staticmethod
    def get_user_data(token):
        return Connection().send_recieve(
            Message(
                Codes.GET_USER_DATA,
                { 'token': token }
            )
        )