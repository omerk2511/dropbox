from common import Codes, Message
from ..handlers.connection import Connection

class GroupController(object):
    @staticmethod
    def create_group(name, token):
        return Connection().send_recieve(
            Message(
                Codes.CREATE_GROUP,
                {
                    'token': token,
                    'name': name
                }
            )
        )

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

    @staticmethod
    def leave_group(group, token):
        return Connection().send_recieve(
            Message(
                Codes.LEAVE_GROUP,
                {
                    'token': token,
                    'group': group
                }
            )
        )