import base64

from common import Codes, Message
from ..handlers.connection import Connection

class FileController(object):
    @staticmethod
    def get_file_content(file_id, token):
        return base64.b64decode(
            Connection().send_recieve(
                Message(
                    Codes.GET_FILE,
                    {
                        'token': token,
                        'file': file_id
                    }
                )
            ).payload['content'])

    @staticmethod
    def create_file(name, directory, content, token):
        return Connection().send_recieve(
            Message(
                Codes.CREATE_FILE,
                {
                    'token': token,
                    'name': name,
                    'directory': directory,
                    'content': base64.b64encode(content)
                }
            )
        )

    @staticmethod
    def delete_file(file_id, token):
        return Connection().send_recieve(
            Message(
                Codes.DELETE_FILE,
                {
                    'token': token,
                    'file': file_id
                }
            )
        )