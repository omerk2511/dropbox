from common import Codes, Message
from controller import controller
from validators import validator, existing_group
from auth import authenticated, group_user
from ..models import Groups, UsersGroups, Directories

CREATE_DIRECTORY_PAYLOAD = [
    ('name', [str, unicode]),
    ('parent', [int]),
    ('group', [str, unicode], True)
]

@controller(Codes.CREATE_DIRECTORY)
@authenticated
@validator(CREATE_DIRECTORY_PAYLOAD)
def create_directory(payload, user):
    name = payload['name']
    group = None

    if 'group' in payload:
        group = payload['group']

        if not Groups.get(group):
            return Message(
                Codes.NOT_FOUND,
                { 'message': 'A group with this id was not found.' }
            )

        if not UsersGroups.is_in_group(user['id'], payload['group']):
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You have to be a group\'s user in order to get information about it.' }
            )

    parent = payload['parent']

    results = Directories.get(parent)

    if not results:
        return Message(
            Codes.NOT_FOUND,
            { 'message': 'The parent directory does not exist.' }
        )

    if group:
        if results[0][3] != group:
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You can\'t create a directory whose parent is not in the same group.' }
            )
    else:
        if results[0][2] != user['id']:
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You can\'t create a directory whose parent is not in your account.' }
            )

    # check that the name of the directory is valid
    # check if there is a directory with the same name

    directory_id = Directories.create(name, user['id'], group, parent)

    return Message(
        Codes.SUCCESS,
        {
            'message': 'The directory has been created successfully.',
            'id': directory_id
        }
    )