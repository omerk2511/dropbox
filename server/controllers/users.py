from common import Codes, Message
from controller import controller

@controller
def log_in(payload):
    return Message(Codes.LOG_IN, { 'status': 'success' })

@controller
def create_user(payload):
    return Message(Codes.CREATE_USER, { 'status': 'success' })