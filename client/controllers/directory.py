from common import Codes, Message
from ..handlers.connection import Connection

class DirectoryController(object):
    @staticmethod
    def create_directory(name, parent, token, group=None):
        """
        Creates a directory
        args: name, parent, token, group
        ret: response
        """

        request = {
            'name': name,
            'parent': parent,
            'token': token
        }

        if group:
            request['group'] = group

        return Connection().send_recieve(
            Message(
                Codes.CREATE_DIRECTORY,
                request
            )
        )

    @staticmethod
    def delete_directory(directory, token):
        """
        Deletes a directory
        args: directory, token
        ret: response
        """

        return Connection().send_recieve(
            Message(
                Codes.DELETE_DIRECTORY,
                {
                    'directory': directory,
                    'token': token
                }
            )
        )

    @staticmethod
    def update_directory_name(directory, name, token):
        """
        Updates a directory name
        args: directory, name, token
        ret: response
        """

        return Connection().send_recieve(
            Message(
                Codes.UPDATE_DIRECTORY,
                {
                    'directory': directory,
                    'name': name,
                    'token': token
                }
            )
        )