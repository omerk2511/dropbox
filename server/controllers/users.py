from common import Codes, Message
from ..handlers.handler import handler

@handler
def log_in(payload):
    return Message(Codes.LOG_IN, { 'status': 'success' })

@handler
def create_user(payload):
    return Message(Codes.CREATE_USER, { 'status': 'success' })