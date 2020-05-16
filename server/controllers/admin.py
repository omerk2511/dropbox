import os

from common import Codes, Message
from controller import controller
from auth import authenticated
from ..models import Logs
from ..config import FILES_PATH

@controller(Codes.GET_ADMIN_DATA)
@authenticated
def get_admin_data(payload, user):
    """
    Returns the administration data
    args: payload, user
    ret: response
    """

    if user['username'] != 'admin':
        return Message(
            Codes.FORBIDDEN,
            { 'message': 'You are not an admin.' }
        )

    used_space = sum(os.path.getsize(FILES_PATH + f) for f in os.listdir(
        FILES_PATH) if os.path.isfile(FILES_PATH + f)) // 1024 ** 2

    return Message(
        Codes.SUCCESS,
        {
            'message': 'Retrieved all the logs successfully.',
            'logs': [
                {
                    'type': log[1],
                    'message': log[2]
                } for log in Logs.get()
            ],
            'used_space': used_space
        }
    )