import sqlite3 as lite

from common import Codes, Message
from controller import controller

@controller(Codes.PING)
def ping(payload):
    """
    Returns an empty response to test connection
    args: payload, user
    ret: response
    """

    return Message(
        Codes.SUCCESS,
        { }
    )