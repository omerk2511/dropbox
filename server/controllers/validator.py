import functools

from common import Codes, Message

def is_payload_valid(payload, rules):
    if type(payload) != dict:
        return False

    for rule in rules:
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