from common import Codes, Message
from controller import controller
from validators import validator, existing_directory, not_existing_file
from auth import authenticated, in_directory_context
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