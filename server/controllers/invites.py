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

    invited_users = [invite[0] for invite in Invites.get_group_invites(payload['group'])]

    if invited_user[0] in invited_users:
        return Message(
            Codes.CONFLICT,
            { 'message': 'This user has already been invited to the group.' }
        )

    Invites.create(invited_user[0], payload['group'])

    return Message(
        Codes.SUCCESS,
        { 'message': 'The requested user has been invited successfully.' }
    )

INVITE_OPERATION_PAYLOAD = [
    ('invite', [int])
]

@controller(Codes.ACCEPT_INVITE)
@authenticated
@validator(INVITE_OPERATION_PAYLOAD)
def accept_invite(payload, user):
    try:
        invite = Invites.get(payload['invite'])[0]
    except:
        return Message(
            Codes.NOT_FOUND,
            { 'message': 'There isn\'t any active invite with the given id.' }
        )

    if user['id'] != invite[1]:
        return Message(
            Codes.FORBIDDEN,
            { 'message': 'This invitation was sent to another user.' }
        )

    UsersGroups.insert(user['id'], invite[2])
    Invites.close(invite[0])

    return Message(
        Codes.SUCCESS,
        { 'message': 'You have successfully joined this group.' }
    )

@controller(Codes.REJECT_INVITE)
@authenticated
@validator(INVITE_OPERATION_PAYLOAD)
def reject_invite(payload, user):
    try:
        invite = Invites.get(payload['invite'])[0]
    except:
        return Message(
            Codes.NOT_FOUND,
            { 'message': 'There isn\'t any active invite with the given id.' }
        )

    if user['id'] != invite[1]:
        return Message(
            Codes.FORBIDDEN,
            { 'message': 'This invitation was sent to another user.' }
        )

    Invites.close(invite[0])

    return Message(
        Codes.SUCCESS,
        { 'message': 'You have successfully reject the invite.' }
    )