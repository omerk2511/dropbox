import jwt
import functools

from common import Codes, Message
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