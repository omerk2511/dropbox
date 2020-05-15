import sqlite3 as lite

from common import Codes, Message
from controller import controller
from validators import validator, existing_group
from auth import authenticated, group_owner, group_user
from ..models import Groups, Users, UsersGroups, Invites, Directories

CREATE_GROUP_PAYLOAD = [
    ('name', [str, unicode])
]

@controller(Codes.CREATE_GROUP)
@authenticated
@validator(CREATE_GROUP_PAYLOAD)
def create_group(payload, user):
    try:
        group_id = Groups.create(payload['name'], user['id'])
        
        Directories.create('/', user['id'], group_id)
        UsersGroups.insert(user['id'], group_id)

        return Message(
            Codes.SUCCESS,
            {
                'message': 'A group has been created successfully.',
                'group': {
                    'id': group_id,
                    'name': payload['name'],
                    'owner': {
                        'id': user['id'],
                        'username': user['username'],
                        'full_name': user['full_name']
                    }
                }
            }
        )
    except lite.IntegrityError:
        return Message(
            Codes.BAD_REQUEST,
            { 'message': 'The requesting user has been deleted.' }
        )

UPDATE_GROUP_PAYLOAD = [
    ('group', [int]),
    [
        ('name', [str, unicode]),
        ('owner', [int])
    ]
]

@controller(Codes.UPDATE_GROUP)
@authenticated
@validator(UPDATE_GROUP_PAYLOAD)
@existing_group
@group_owner
def update_group(payload, user):
    if 'name' in payload:
        Groups.update_name(payload['group'], payload['name'])

    if 'owner' in payload:
        Groups.update_owner(payload['group'], payload['owner'])

        UsersGroups.delete(user['id'], payload['group'])
        UsersGroups.insert(user['id'], payload['group'])

    return Message(
        Codes.SUCCESS,
        { 'message': 'The group has been updated successfully.' }
    )

DELETE_GROUP_PAYLOAD = [
    ('group', [int])
]

@controller(Codes.DELETE_GROUP)
@authenticated
@validator(DELETE_GROUP_PAYLOAD)
@existing_group
@group_owner
def delete_group(payload, user):
    Groups.delete(payload['group']) # also delete files later

    return Message(
        Codes.SUCCESS,
        { 'message': 'The group has been deleted successfully.' }
    )

GET_GROUP_DATA_PAYLOAD = [
    ('group', [int])
]

@controller(Codes.GET_GROUP_DATA)
@authenticated
@validator(GET_GROUP_DATA_PAYLOAD)
@existing_group
@group_user
def get_group_data(payload, user):
    group = Groups.get(payload['group'])[0]
    owner = Users.get(group[2])[0]

    return Message(
        Codes.SUCCESS,
        {
            'message': 'The group data has been retrieved successfully.',
            'id': payload['group'],
            'name': group[1],
            'owner': {
                'id': group[2],
                'username': owner[1],
                'full_name': owner[2]
            },
            'invites': [
                {
                    'id': invite[4],
                    'user': {
                        'id': invite[0],
                        'username': invite[1],
                        'full_name': invite[2]
                    }
                } for invite in Invites.get_group_invites(payload['group'])
            ],
            'users': [
                {
                    'id': user[0],
                    'username': user[1],
                    'full_name': user[2]
                } for user in UsersGroups.get_users(payload['group'])
            ],
            'files': Directories.get_group_directory_tree(payload['group'])
        }
    )

LEAVE_GROUP_PAYLOAD = [
    ('group', [int])
]

@controller(Codes.LEAVE_GROUP)
@authenticated
@validator(LEAVE_GROUP_PAYLOAD)
@existing_group
@group_user
def leave_group(payload, user):
    group = Groups.get(payload['group'])[0]
    owner = group[2]

    if user['id'] == owner:
        return Message(
            Codes.FORBIDDEN,
            { 'message': 'You can\'t leave a group that you own.' }
        )

    # also update the files' owner
    Directories.update_owner_in_group(user['id'], owner, payload['group'])

    UsersGroups.delete(user['id'], payload['group'])

    return Message(
        Codes.SUCCESS,
        { 'message': 'You have left the group successfully.' }
    )