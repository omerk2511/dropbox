from common import Codes, Message
from ..handlers.connection import Connection

class DirectoryController(object):
    @staticmethod
    def create_directory(name, parent, token, group=None):
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