import sqlite3 as lite

from common import Codes, Message
from controller import controller
from validator import validator
from ..models import Users

@controller(Codes.LOG_IN)
@validator([
    ('username', [str, unicode]),
    ('password', [str, unicode])])
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

@controller(Codes.CREATE_USER)
@validator([
    ('username', [str, unicode]),
    ('full_name', [str, unicode]),
    ('password', [str, unicode])])
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