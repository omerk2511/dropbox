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
    def get_file_extension(file_id, token):
        file_data = Connection().send_recieve(
            Message(
                Codes.GET_FILE,
                {
                    'token': token,
                    'file': file_id
                }
            )
        ).payload

        splitted_file_name = file_data['name'].split('.')

        if len(splitted_file_name) > 1:
            return splitted_file_name[-1]

        return None

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