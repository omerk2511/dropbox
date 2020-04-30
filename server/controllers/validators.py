import functools

from common import Codes, Message
from ..models import Groups

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
            if rule[0] not in payload or type(payload[rule[0]]) not in rule[1]:
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