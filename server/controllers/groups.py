import jwt
import sqlite3 as lite

from common import Codes, Message
from controller import controller
from validator import validator
from ..config import JWT_SECRET_KEY
from ..models import Groups

CREATE_GROUP_PAYLOAD = [
    ('token', [str, unicode]),
    ('name', [str, unicode])
]

@controller(Codes.CREATE_GROUP)
@validator(CREATE_GROUP_PAYLOAD)
def create_group(payload):
    try:
        user_id = jwt.decode(payload['token'], JWT_SECRET_KEY, algorithm='HS256')['id']
    except:
        return Message(
            Codes.FORBIDDEN,
            { 'message': 'The supplied token is not valid.' }
        )

    try:
        Groups.create(payload['name'], user_id)

        return Message(
            Codes.SUCCESS,
            { 'message': 'A group was created successfully!' }
        )
    except lite.IntegrityError:
        return Message(
            Codes.BAD_REQUEST,
            { 'message': 'The requesting user has been deleted.' }
        )