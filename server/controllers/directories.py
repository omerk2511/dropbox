from common import Codes, Message
from controller import controller
from validators import validator, existing_directory
from auth import authenticated, directory_editor, is_directory_owner
from ..models import Groups, UsersGroups, Directories

CREATE_DIRECTORY_PAYLOAD = [
    ('name', [str, unicode]),
    ('parent', [int]),
    ('group', [int], True)
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
                { 'message': 'You have to be a group\'s user in order to create a directory in it.' }
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
        if results[0][3]:
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You can\'t create a personal directory whose parent is in a group.' }
            )

        if results[0][2] != user['id']:
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You can\'t create a directory whose parent is not in your account.' }
            )

    if group:
        directories = Directories.get_group_directories_under_parent(group, parent)
    else:
        directories = Directories.get_user_directories_under_parent(user['id'], parent)

    if name in [directory[1] for directory in directories]:
        return Message(
            Codes.CONFLICT,
            { 'message': 'There is already a directory with the same name.' }
        )

    directory_id = Directories.create(name, user['id'], group, parent)

    return Message(
        Codes.SUCCESS,
        {
            'message': 'The directory has been created successfully.',
            'id': directory_id
        }
    )

UPDATE_DIRECTORY_PAYLOAD = [
    ('directory', [int]),
    [
        ('name', [str, unicode]),
        ('owner', [int]),
        ('parent', [int])
    ]
]

@controller(Codes.UPDATE_DIRECTORY)
@authenticated
@validator(UPDATE_DIRECTORY_PAYLOAD)
@existing_directory
@directory_editor
def update_directory(payload, user):
    group = Directories.get(payload['directory'])[0][3]

    if 'owner' in payload or 'parent' in payload:
        if not is_directory_owner(payload['directory'], user['id']):
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You cannot change the location or the owner of a directory you do not own.' }
            )

    if 'name' in payload:
        if group:
            directories = Directories.get_user_directories(user['id'])
        else:
            directories = Directories.get_group_directories(group)

        if payload['name'] in [directory[1] for directory in directories]:
            return Message(
                Codes.CONFLICT,
                { 'message': 'There is already a directory with the same name.' }
            )

    if 'owner' in payload:
        if group:
            if not UsersGroups.is_in_group(payload['owner'], group):
                return Message(
                    Codes.BAD_REQUEST,
                    { 'message': 'You cannot give ownership of a directory to a user that is not a member of the group in which the directory resides.' }
                )
        else:
            return Message(
                Codes.BAD_REQUEST,
                { 'message': 'You cannot transfer a personal directory to another user.' }
            )

    if 'parent' in payload:
        if group:
            directories = Directories.get_group_directories(group)
        else:
            directories = Directories.get_user_directories(user['id'])

        if payload['parent'] not in [directory[0] for directory in directories]:
            return Message(
                Codes.NOT_FOUND,
                { 'message': 'The given parent directory does not exist in the directory\'s context.' }
            )

    if 'name' in payload:
        Directories.update_name(payload['directory'], payload['name'])

    if 'owner' in payload:
        Directories.update_owner(payload['directory'], payload['owner'])

    if 'parent' in payload:
        Directories.update_parent(payload['directory'], payload['parent'])

    return Message(
        Codes.SUCCESS,
        { 'message': 'The directory has been updated successfully.' }
    )