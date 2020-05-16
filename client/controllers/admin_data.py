from common import Codes, Message
from ..handlers.connection import Connection

class AdminDataController(object):
    @staticmethod
    def get_admin_data(token):
        return Connection().send_recieve(
            Message(
                Codes.GET_ADMIN_DATA,
                { 'token': token }
            )
        )