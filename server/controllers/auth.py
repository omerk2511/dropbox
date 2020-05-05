import jwt
import functools

from common import Codes, Message
from ..models import Groups, UsersGroups
from ..config import JWT_SECRET_KEY

def authenticated(func):
    @functools.wraps(func)
    def wrapper(payload):
        try:
            user = jwt.decode(payload['token'], JWT_SECRET_KEY, algorithm='HS256')
        except:
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'A token was not supplied or not valid.' }
            )

        del payload['token']
        return func(payload, user)

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
        if not UsersGroups.is_in_group(user['id'], payload['group']):
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You have to be a group\'s user in order to get information about it.' }
            )

        return func(payload, user, *args, **kwargs)

    return wrapper

def directory_owner(func):
    @functools.wraps(func)
    def wrapper(payload, user, *args, **kwargs):
        directory = Directories.get(payload['directory'])[0]
        owner = directory[2]

        if user['id'] != owner:
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You have to be a directory\'s owner in order to modify it.' }
            )

        return func(payload, user, *args, **kwargs)

    return wrapper