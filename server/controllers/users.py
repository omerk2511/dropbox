import sqlite3 as lite

from common import Codes, Message
from controller import controller
from validators import validator
from auth import authenticated
from ..models import Users, Invites, UsersGroups

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

@controller(Codes.GET_USER_DATA)
@authenticated
def get_user_data(payload, user):
    user_data = user.copy()

    user_data['groups'] = [
        {
            'id': group[0],
            'name': group[1],
            'owner': {
                'username': Users.get(group[2])[0][1],
                'full_name': Users.get(group[2])[0][2]
            }
        } for group in UsersGroups.get_groups(user['id'])
    ]

    user_data['invites'] = [
        {
            'id': invite[3],
            'group': {
                'id': invite[0],
                'name': invite[1],
                'owner': {
                    'username': Users.get(invite[2])[0][1],
                    'full_name': Users.get(invite[2])[0][2]
                }
            }
        } for invite in Invites.get_user_invites(user['id'])
    ]

    # files - later

    return Message(
        Codes.SUCCESS,
        dict(message='User data has been retrieved successfully.', **user_data)
    )