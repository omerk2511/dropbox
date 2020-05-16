from common import Codes, Message
from controller import controller
from validators import validator, existing_directory, existing_file, not_existing_file
from auth import authenticated, in_directory_context, in_file_context, file_owner, is_file_editor, file_editor
from ..models import Groups, UsersGroups, Directories, Files

CREATE_FILE_PAYLOAD = [
    ('name', [str, unicode]),
    ('directory', [int]),
    ('content', [str, unicode])
]   

@controller(Codes.CREATE_FILE)
@authenticated
@validator(CREATE_FILE_PAYLOAD)
@existing_directory
@in_directory_context
@not_existing_file
def create_file(payload, user):
    """
    Creates a file
    args: payload, user
    ret: response
    """

    file_id = Files.create(payload['name'], user['id'], payload['directory'])
    Files.write(file_id, payload['content'])

    return Message(
        Codes.SUCCESS,
        {
            'message': 'Create the file successfully.',
            'id': file_id
        }
    )

UPDATE_FILE_PAYLOAD = [
    ('file', [int]),
    [
        ('name', [str, unicode]),
        ('content', [str, unicode])
    ]
]

@controller(Codes.UPDATE_FILE)
@authenticated
@validator(UPDATE_FILE_PAYLOAD)
@existing_file
@file_editor
def update_file(payload, user):
    """
    Updates a file
    args: payload, user
    ret: response
    """

    if 'name' in payload:
        Files.update_name(payload['file'], payload['name'])

    if 'content' in payload:
        Files.write(payload['file'], payload['content'])

    return Message(
        Codes.SUCCESS,
        { 'message': 'The file has been updated successfully.' }
    )

DELETE_FILE_PAYLOAD = [
    ('file', [int])
]

@controller(Codes.DELETE_FILE)
@authenticated
@validator(DELETE_FILE_PAYLOAD)
@existing_file
@file_owner
def delete_file(payload, user):
    """
    Deletes a file
    args: payload, user
    ret: response
    """

    Files.delete(payload['file'])

    return Message(
        Codes.SUCCESS,
        { 'message': 'The file has been deleted successfully.' }
    )

GET_FILE_PAYLOAD = [
    ('file', [int])
]

@controller(Codes.GET_FILE)
@authenticated
@validator(GET_FILE_PAYLOAD)
@existing_file
@in_file_context
def get_file(payload, user):
    """
    Returns a file
    args: payload, user
    ret: response
    """

    f = Files.get(payload['file'])[0]
    content = Files.read(payload['file'])

    return Message(
        Codes.SUCCESS,
        {
            'message': 'Retrieved the file successfully.',
            'id': f[0],
            'name': f[2],
            'owner': f[3],
            'directory': f[4],
            'content': content
        }
    )