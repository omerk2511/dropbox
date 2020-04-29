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
                'message': 'A group was created successfully!',
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