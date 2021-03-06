import sqlite3 as lite

from common import Codes, Message
from controller import controller
from validators import validator
from auth import authenticated
from ..models import Users, Invites, UsersGroups, Directories

LOG_IN_PAYLOAD = [
    ('username', [str, unicode]),
    ('password', [str, unicode])
]

@controller(Codes.LOG_IN)
@validator(LOG_IN_PAYLOAD)
def log_in(payload):
    """
    Logs a user in
    args: payload, user
    ret: response
    """

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
    """
    Creates a user
    args: payload, user
    ret: response
    """

    try:
        user_id = Users.create(**payload)
        Directories.create('/', user_id)

        return Message(
            Codes.SUCCESS,
            { 'message': 'A user was created successfully!' }
        )
    except lite.IntegrityError:
        return Message(
            Codes.CONFLICT,
            { 'message': 'A user with this username already exists.' }
        )

UPDATE_USER_PAYLOAD = [
    [
        ('full_name', [str, unicode]),
        ('password', [str, unicode])
    ]
]

@controller(Codes.UPDATE_USER)
@authenticated
@validator(UPDATE_USER_PAYLOAD)
def update_user(payload, user):
    """
    Updates a user
    args: payload, user
    ret: response
    """

    if 'full_name' in payload:
        Users.update_full_name(user['id'], payload['full_name'])

    if 'password' in payload:
        Users.update_password(user['id'], payload['password'])

    return Message(
        Codes.SUCCESS,
        {
            'message': 'The user has been updated successfully.',
            'token': Users.get_jwt(user['id'])
        }
    )

@controller(Codes.GET_USER_DATA)
@authenticated
def get_user_data(payload, user):
    """
    Retrieves the data of the current user
    args: payload, user
    ret: response
    """

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

    user_data['files'] = Directories.get_user_directory_tree(user['id'])

    return Message(
        Codes.SUCCESS,
        dict(message='User data has been retrieved successfully.', **user_data)
    )