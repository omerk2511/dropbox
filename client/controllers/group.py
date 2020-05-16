from common import Codes, Message
from ..handlers.connection import Connection

class GroupController(object):
    @staticmethod
    def create_group(name, token):
        """
        Creates a group
        args: name, token
        ret: response
        """

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
        """
        Gets a group data
        args: group, token
        ret: response
        """

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
        """
        Leaves a group
        args: group, token
        ret: response
        """

        return Connection().send_recieve(
            Message(
                Codes.LEAVE_GROUP,
                {
                    'token': token,
                    'group': group
                }
            )
        )

    @staticmethod
    def update_group(group, token, name=None, owner=None):
        """
        Updates a group
        args: group, token, name, owner
        ret: response
        """

        request = {
            'group': group,
            'token': token
        }

        if name:
            request['name'] = name

        if owner:
            request['owner'] = owner

        return Connection().send_recieve(
            Message(
                Codes.UPDATE_GROUP,
                request
            )
        )

    @staticmethod
    def kick_group_user(group, user, token):
        """
        Kicks a group user
        args: group, user, token
        ret: response
        """

        return Connection().send_recieve(
            Message(
                Codes.KICK_GROUP_USER,
                {
                    'group': group,
                    'user': user,
                    'token': token
                }
            )
        )