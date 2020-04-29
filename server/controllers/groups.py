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
        Groups.create(payload['name'], user['id'])

        return Message(
            Codes.SUCCESS,
            { 'message': 'A group was created successfully!' }
        )
    except lite.IntegrityError:
        return Message(
            Codes.BAD_REQUEST,
            { 'message': 'The requesting user has been deleted.' }
        )