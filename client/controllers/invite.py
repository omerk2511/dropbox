from common import Codes, Message
from ..handlers.connection import Connection

class InviteController(object):
    @staticmethod
    def invite(group_id, username, token):
        """
        Creates an invite
        args: group_id, username, token
        ret: response
        """

        return Connection().send_recieve(
            Message(
                Codes.INVITE,
                {
                    'token': token,
                    'group': group_id,
                    'username': username
                }
            )
        )

    @staticmethod
    def accept_invite(invite_id, token):
        """
        Accepts an invite
        args: invite_id, token
        ret: response
        """

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
        """
        Rejects an invite
        args: invite_id, token
        ret: response
        """

        return Connection().send_recieve(
            Message(
                Codes.REJECT_INVITE,
                {
                    'token': token,
                    'invite': invite_id
                }
            )
        )

    @staticmethod
    def revoke_invite(invite_id, token):
        """
        Revokes an invite
        args: invite_id, token
        ret: response
        """

        return Connection().send_recieve(
            Message(
                Codes.REVOKE_INVITE,
                {
                    'token': token,
                    'invite': invite_id
                }
            )
        )