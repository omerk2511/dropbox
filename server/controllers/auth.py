import jwt
import functools

from common import Codes, Message
from ..models import Groups, UsersGroups, Directories, Files, Editors
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

def is_directory_owner(directory_id, user_id):
    directory = Directories.get(directory_id)[0]

    owner = directory[2]
    group = directory[3]

    is_owner = user_id == owner

    if group:
        is_group_owner = user_id == Groups.get(group)[0][2]
        is_owner = is_owner or is_group_owner

    return is_owner

def directory_owner(func):
    @functools.wraps(func)
    def wrapper(payload, user, *args, **kwargs):
        if not is_directory_owner(payload['directory'], user['id']):
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You have to be a directory\'s owner in order to modify it.' }
            )

        return func(payload, user, *args, **kwargs)

    return wrapper

def is_directory_editor(directory_id, user_id):
    is_editor = Editors.is_directory_editor(user_id, directory_id)
    is_editor = is_editor or is_directory_owner(directory_id, user_id)

    return is_editor

def directory_editor(func):
    @functools.wraps(func)
    def wrapper(payload, user, *args, **kwargs):
        if not is_directory_editor(payload['directory'], user['id']):
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You have to be a directory\'s editor in order to modify it.' }
            )
        
        return func(payload, user, *args, **kwargs)

    return wrapper

def is_in_directory_context(directory_id, user_id):
    directory = Directories.get(directory_id)[0]

    owner = directory[2]
    group = directory[3]

    if group:
        if not UsersGroups.is_in_group(user_id, group):
            return False
    else:
        if user_id != owner:
            return False

    return True

def in_directory_context(func):
    @functools.wraps(func)
    def wrapper(payload, user, *args, **kwargs):
        if not is_in_directory_context(payload['directory'], user['id']):
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You are not in the directory\'s context.' }
            )

        return func(payload, user, *args, **kwargs)

    return wrapper

def is_file_owner(file_id, user_id):
    f = Files.get(file_id)[0]
    directory = Directories.get(f[4])[0]
    group_id = directory[3]

    file_owner = user_id == f[3] or user_id == directory[2]

    if group_id:
        group = Groups.get(group_id)[0]
        file_owner = file_owner or user_id == group[2]

    return file_owner

def file_owner(func):
    @functools.wraps(func)
    def wrapper(payload, user, *args, **kwargs):
        if not is_file_owner(payload['file'], user['id']):
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You have to be a file\'s owner in order to modify it.' }
            )

        return func(payload, user, *args, **kwargs)

    return wrapper

def is_file_editor(file_id, user_id):
    is_editor = Editors.is_file_editor(user_id, file_id)
    is_editor = is_editor or is_file_owner(file_id, user_id)

    return is_editor

def file_editor(func):
    @functools.wraps(func)
    def wrapper(payload, user, *args, **kwargs):
        if not is_file_editor(payload['file'], user['id']):
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You have to be a file\'s editor in order to modify it.' }
            )

        return func(payload, user, *args, **kwargs)

    return wrapper

def is_in_file_context(file_id, user_id):
    f = Files.get(file_id)[0]
    directory = Directories.get(f[4])[0]

    owner = directory[2]
    group = directory[3]

    if group:
        if not UsersGroups.is_in_group(user_id, group):
            return False
    else:
        if user_id != owner:
            return False

    return True

def in_file_context(func):
    @functools.wraps(func)
    def wrapper(payload, user, *args, **kwargs):
        if not is_in_file_context(payload['file'], user['id']):
            return Message(
                Codes.FORBIDDEN,
                { 'message': 'You are not in the file\'s context.' }
            )

        return func(payload, user, *args, **kwargs)

    return wrapper