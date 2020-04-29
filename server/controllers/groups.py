import sqlite3 as lite

from common import Codes, Message
from controller import controller
from validator import validator
from auth import authenticated
from ..models import Groups

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
def update_group(payload, user):
    groups = Groups.get(payload['group'])

    if not groups:
        return Message(
            Codes.NOT_FOUND,
            { 'message': 'A group with this id was not found.' }
        )

    owner = groups[0][2]

    if user['id'] != owner:
        return Message(
            Codes.FORBIDDEN,
            { 'message': 'You have to be a group\'s owner in order to update it.' }
        )

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
def delete_group(payload, user):
    groups = Groups.get(payload['group'])

    if not groups:
        return Message(
            Codes.NOT_FOUND,
            { 'message': 'A group with this id was not found.' }
        )

    owner = groups[0][2]

    if user['id'] != owner:
        return Message(
            Codes.FORBIDDEN,
            { 'message': 'You have to be a group\'s owner in order to update it.' }
        )

    Groups.delete(payload['group']) # also delete files later

    return Message(
        Codes.SUCCESS,
        { 'message': 'The group has been deleted successfully.' }
    )