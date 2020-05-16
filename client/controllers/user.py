from common import Codes, Message
from ..handlers.connection import Connection

class UserController(object):
    @staticmethod
    def get_user_data(token):
        """
        Gets the current user's data
        args: token
        ret: response
        """

        return Connection().send_recieve(
            Message(
                Codes.GET_USER_DATA,
                { 'token': token }
            )
        )

    @staticmethod
    def update_user(token, full_name=None, password=None):
        """
        Updates the current user
        args: token, full_name, password
        ret: response
        """

        request = Message(
            Codes.UPDATE_USER,
            { 'token': token }
        )
        
        if full_name:
            request.payload['full_name'] = full_name

        if password:
            request.payload['password'] = password

        return Connection().send_recieve(request)