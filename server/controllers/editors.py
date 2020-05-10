from common import Codes, Message
from controller import controller
from validators import validator, file_exists, directory_exists, existing_editor
from auth import authenticated, is_file_owner, is_in_file_context, is_directory_owner, is_in_directory_context
from ..models import Users, Editors

ADD_EDITOR_PAYLOAD = [
    ('user', [int]),
    [
        ('file', [int]),
        ('directory', [int])
    ]
]

@controller(Codes.ADD_EDITOR)
@authenticated
@validator(ADD_EDITOR_PAYLOAD)
def add_editor(payload, user):
    if 'file' in payload and 'directory' in payload:
        return Message(
            Codes.BAD_REQUEST,
            { 'message': 'Invalid payload. You should supply either a file or a directory, not both.' }
        )

    editor_id = payload['user']

    if 'file' in payload:
        if not file_exists(payload['file']):
            return Message(
                Codes.NOT_FOUND,
                { 'message': 'The supplied file does not exist.' }
            )

        if not is_file_owner(payload['file'], user['id']):
            return Message(
                Codes.FORBIDDEN,
                { 'message':'You cannot share a file you do not own.' }
            )

        if not is_in_file_context(payload['file'], editor_id):
            return Message(
                Codes.BAD_REQUEST,
                { 'message': 'You cannot share a file with someone who is not in the file\'s context.' }
            )

        Editors.create(editor_id, file_id=payload['file'])

    if 'directory' in payload:
        if not directory_exists(payload['directory']):
            return Message(
                Codes.NOT_FOUND,
                { 'message': 'The supplied directory does not exist.' }
            )

        if not is_directory_editor(paylaod['directory'], user['id']):
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You cannot share a directory you do not own.' }
            )

        if not is_in_directory_context(paylaod['directory'], editor_id):
            return Message(
                Codes.BAD_REQUEST,
                { 'message': 'You cannot share a directory with someone who is not in the directory\'s context.' }
            )

        Editors.create(editor_id, directory_id=payload['directory'])

    return Message(
        Codes.SUCCESS,
        { 'message': 'The file / directory has been shared successfully.' }
    )

REMOVE_EDITOR_PAYLOAD = [
    ('editor', [int])
]

@controller(Codes.REMOVE_EDITOR)
@authenticated
@validator(REMOVE_EDITOR_PAYLOAD)
@existing_editor
def remove_editor(payload, user):
    editor = Editors.get(payload['editor'])[0]

    file_id = editor[2]
    directory_id = editor[3]

    if file_id:
        if not is_file_owner(file_id, user['id']):
            return Message(
                Codes.FORBIDDEN,
                { 'message':'You cannot modify a file you do not own.' }
            )
    else:
        if not is_directory_editor(directory_id, user['id']):
            return Message(
                Codes.FORBIDDEN,
                { 'message':'You cannot modify a directory you do not own.' }
            )

    Editors.delete(payload['editor'])

    return Message(
        Codes.SUCCESS,
        { 'message': 'The editor has been removed successfully.' }
    )