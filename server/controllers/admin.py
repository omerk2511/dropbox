from common import Codes, Message
from controller import controller
from auth import authenticated

@controller(Codes.GET_ADMIN_DATA)
@authenticated
def get_admin_data(payload, user):
    if user['username'] != 'admin':
        return Message(
            Codes.FORBIDDEN,
            { 'message': 'You are not an admin.' }
        )