from common import Codes, Message
from ..handlers.connection import Connection

class InviteController(object):
    @staticmethod
    def accept_invite(invite_id, token):
        return Connection().send_recieve(
            Message(
                Codes.ACCEPT_INVITE,
                {
                    'token': token,
                    'invite': invite_id
                }
            )
        )

    @staticmethod
    def reject_invite(invite_id, token):
        return Connection().send_recieve(
            Message(
                Codes.REJECT_INVITE,
                {
                    'token': token,
                    'invite': invite_id
                }
            )
        )