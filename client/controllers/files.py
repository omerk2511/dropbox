import base64

from common import Codes, Message
from ..handlers.connection import Connection

class FileController(object):
    @staticmethod
    def get_file_content(file_id, token):
        """
        Gets a file content
        args: file_id, token
        ret: content
        """

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
        """
        Creates a file
        args: name, directory, content, token
        ret: response
        """

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
        """
        Deletes a file
        args: file_id, token
        ret: response
        """

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
        """
        Returns whether the current user is a file editor
        args: file_id, token
        ret: response
        """

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
    def update_file(file_id, token, name=None, content=None):
        """
        Updates a file
        args: file_id, token, name, content
        ret: response
        """

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

    @staticmethod
    def get_file_editors(file_id, token):
        """
        Gets the editors of a file
        args: file_id, token
        ret: editors
        """

        return Connection().send_recieve(
            Message(
                Codes.GET_EDITORS,
                {
                    'token': token,
                    'file': file_id
                }
            )
        ).payload['editors']

    @staticmethod
    def add_file_editor(file_id, user, token):
        """
        Adds a file editor
        args: file_id, user, token
        ret: response
        """

        return Connection().send_recieve(
            Message(
                Codes.ADD_EDITOR,
                {
                    'token': token,
                    'file': file_id,
                    'user': user
                }
            )
        )

    @staticmethod
    def remove_file_editor(editor_id, token):
        """
        Removes a file editor
        args: editor_id, token
        ret: response
        """

        return Connection().send_recieve(
            Message(
                Codes.REMOVE_EDITOR,
                {
                    'token': token,
                    'editor': editor_id
                }
            )
        )