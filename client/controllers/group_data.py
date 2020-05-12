from common import Codes, Message
from ..handlers.connection import Connection

class GroupDataController(object):
    @staticmethod
    def get_group_data(group, token):
        return Connection().send_recieve(
            Message(
                Codes.GET_GROUP_DATA,
                {
                    'token': token,
                    'group': group
                }
            )
        )