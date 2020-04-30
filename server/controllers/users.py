import sqlite3 as lite

from common import Codes, Message
from controller import controller
from validators import validator
from ..models import Users

LOG_IN_PAYLOAD = [
    ('username', [str, unicode]),
    ('password', [str, unicode])
]

@controller(Codes.LOG_IN)
@validator(LOG_IN_PAYLOAD)
def log_in(payload):
    token = Users.log_in(**payload)

    if token:
        return Message(
            Codes.SUCCESS,
            {
                'message': 'You have logged in successfully.',
                'token': token
            }
        )
    else:
        return Message(
            Codes.UNAUTHORIZED,
            { 'message': 'The credentials you have provided are invalid.' }
        )

CREATE_USER_PAYLOAD = [
    ('username', [str, unicode]),
    ('full_name', [str, unicode]),
    ('password', [str, unicode])
]

@controller(Codes.CREATE_USER)
@validator(CREATE_USER_PAYLOAD)
def create_user(payload):
    try:
        Users.create(**payload)

        return Message(
            Codes.SUCCESS,
            { 'message': 'A user was created successfully!' }
        )
    except lite.IntegrityError:
        return Message(
            Codes.CONFLICT,
            { 'message': 'A user with this username already exists.' }
        )