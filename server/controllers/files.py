from common import Codes, Message
from controller import controller
from validators import validator, existing_directory, existing_file, not_existing_file
from auth import authenticated, in_directory_context, in_file_context
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
    file_id = Files.create(payload['name'], user['id'], payload['directory'])
    Files.write(file_id, payload['content'])

    return Message(
        Codes.SUCCESS,
        {
            'message': 'Create the file successfully.',
            'id': file_id
        }
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