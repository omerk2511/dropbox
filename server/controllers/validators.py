import functools

from common import Codes, Message
from ..models import Groups, Directories, Files

def is_payload_valid(payload, rules):
    if type(payload) != dict:
        return False

    for rule in rules:
        if type(rule) == list:
            count = 0

            for nested_rule in rule:
                count += 1 if (nested_rule[0] in payload and type(
                    payload[nested_rule[0]]) in nested_rule[1]) else 0

            if count == 0:
                return False
        else:
            if (rule[0] not in payload or type(payload[rule[0]])
                not in rule[1]) and (len(rule) == 2 or not rule[2]):
                return False

    return True

def validator(rules):
    def validation_decorator(func):
        @functools.wraps(func)
        def validation_wrapper(payload, *args, **kwargs):
            if is_payload_valid(payload, rules):
                return func(payload, *args, **kwargs)
            else:
                return Message(
                    Codes.BAD_REQUEST,
                    { 'message': 'The requests\'s payload is invalid.' }
                )

        return validation_wrapper

    return validation_decorator

def existing_group(func):
    @functools.wraps(func)
    def wrapper(payload, *args, **kwargs):
        groups = Groups.get(payload['group'])

        if not groups:
            return Message(
                Codes.NOT_FOUND,
                { 'message': 'A group with this id was not found.' }
            )

        return func(payload, *args, **kwargs)

    return wrapper

def directory_exists(directory_id):
    directories = Directories.get(directory_id)
    return True if directories else False

def existing_directory(func):
    @functools.wraps(func)
    def wrapper(payload, *args, **kwargs):
        if not directory_exists(payload['directory']):
            return Message(
                Codes.NOT_FOUND,
                { 'message': 'A directory with this id was not found.' }
            )

        return func(payload, *args, **kwargs)

    return wrapper

def file_exists(file_id):
    files = Files.get(file_id)
    return True if files else False

def existing_file(func):
    @functools.wraps(func)
    def wrapper(payload, *args, **kwargs):
        if not file_exists(payload['file']):
            return Message(
                Codes.NOT_FOUND,
                { 'message': 'There is no file with this id.' }
            )

        return func(payload, *args, **kwargs)

    return wrapper

def not_existing_file(func):
    @functools.wraps(func)
    def wrapper(payload, *args, **kwargs):
        files = Files.get_directory_files(payload['directory'])

        if payload['name'] in [f[2] for f in files]:
            return Message(
                Codes.CONFLICT,
                { 'message': 'There is already a file with the same name in the directory.' }
            )

        return func(payload, *args, **kwargs)

    return wrapper