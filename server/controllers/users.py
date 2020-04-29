import sqlite3 as lite

from common import Codes, Message
from controller import controller
from ..models import Users

def is_payload_valid(payload, rules):
    if type(payload) != dict:
        return False

    for rule in rules:
        if rule[0] not in payload or type(payload[rule[0]]) not in rule[1]:
            return False

    return True

@controller
def log_in(payload):
    rules = [
        ('username', [str, unicode]),
        ('password', [str, unicode])
    ]

    if not is_payload_valid(payload, rules):
        return Message(
            Codes.BAD_REQUEST,
            { 'message': 'A username and a password should be provided.' }
        )

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

@controller
def create_user(payload):
    rules = [
        ('username', [str, unicode]),
        ('full_name', [str, unicode]),
        ('password', [str, unicode])
    ]

    if not is_payload_valid(payload, rules):
        return Message(
            Codes.BAD_REQUEST,
            { 'message': 'A username, a full name, and a password should be provided.' }
        )

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