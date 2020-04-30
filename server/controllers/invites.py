import functools
import sqlite3 as lite

from common import Codes, Message
from controller import controller
from validators import validator, existing_group
from auth import authenticated, group_owner
from ..models import Groups, Users, UsersGroups, Invites

INVITE_PAYLOAD = [
    ('group', [int]),
    ('username', [str, unicode])
]

@controller(Codes.INVITE)
@authenticated
@validator(INVITE_PAYLOAD)
@existing_group
@group_owner
def invite(payload, user):
    try:
        invited_user = Users.get_by_username(payload['username'])[0]
    except:
        return Message(
            Codes.NOT_FOUND,
            { 'message': 'There isn\'t any user with the given username.' }
        )

    Invites.create(invited_user[0], payload['group'])

    return Message(
        Codes.SUCCESS,
        { 'message': 'The requested user has been invited successfully.' }
    )