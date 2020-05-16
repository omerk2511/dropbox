import base64

from common import Codes, Message
from ..handlers.connection import Connection

class FileController(object):
    @staticmethod
    def get_file_content(file_id, token):
        response = Connection().send_recieve(
            Message(
                Codes.GET_FILE,
                {
                    'token': token,
                    'file': file_id
                }
            )
        )

        if response.code == Codes.SUCCESS:
            return base64.b64decode(response.payload['content'])
        
        raise Exception(response.payload['message'])

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

    @staticmethod
    def is_file_editor(file_id, token):
        try:
            return Connection().send_recieve(
                Message(
                    Codes.IS_FILE_EDITOR,
                    {
                        'token': token,
                        'file': file_id
                    }
                )
            ).payload['is_file_editor']
        except:
            return False

    @staticmethod
    def get_file_editors(file_id, token):
        return Connection().send_recieve(
            Message(
                Codes.GET_EDITORS,
                {
                    'token': token,
                    'file': file_id
                }
            )
        )

    @staticmethod
    def update_file(file_id, token, name=None, content=None):
        request = {
            'token': token,
            'file': file_id
        }

        if name:
            request['name'] = name

        if content:
            request['content'] = base64.b64encode(content)

        return Connection().send_recieve(
            Message(
                Codes.UPDATE_FILE,
                request
            )
        )