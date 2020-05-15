import sqlite3 as lite

from common import Codes, Message
from controller import controller

@controller(Codes.PING)
def log_in(payload):
    return Message(
        Codes.SUCCESS,
        { }
    )