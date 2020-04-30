import functools
import sqlite3 as lite

from common import Codes, Message
from controller import controller
from validator import validator
from auth import authenticated
from ..models import Groups, Users

def existing_group(func):
    @functools.wraps(func)
    def wrapper(payload, *args, **kwargs):
        groups = Groups.get(payload['group'])

        if not groups:
            return Message(
                Codes.NOT_FOUND,
                { 'message': 'A group with this id was not found.' }
            )

        return func(payload, *args, **kwargs)

    return wrapper

def group_owner(func):
    @functools.wraps(func)
    def wrapper(payload, user, *args, **kwargs):
        group = Groups.get(payload['group'])[0]
        owner = group[2]

        if user['id'] != owner:
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You have to be a group\'s owner in order to modify it.' }
            )

        return func(payload, user, *args, **kwargs)
    
    return wrapper

def group_user(func):
    @functools.wraps(func)
    def wrapper(payload, user, *args, **kwargs):
        # validate that the user is a group user
        return func(payload, user, *args, **kwargs)

    return wrapper

CREATE_GROUP_PAYLOAD = [
    ('name', [str, unicode])
]

@controller(Codes.CREATE_GROUP)
@authenticated
@validator(CREATE_GROUP_PAYLOAD)
def create_group(payload, user):
    try:
        group_id = Groups.create(payload['name'], user['id'])

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
            'group': {
                'id': group[0],
                'name': group[1],
                'owner': {
                    'id': group[2],
                    'username': owner[1],
                    'full_name': owner[2]
                }
            }
        }
    )