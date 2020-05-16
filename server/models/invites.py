from initialization import initializer
from ..handlers.database import database

class Invites(object):
    @staticmethod
    @initializer
    def initialize():
        """
        Initializes the invites table
        args: none
        ret: none
        """

        database.execute(
            '''
            CREATE TABLE IF NOT EXISTS invites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                revoked BOOLEAN DEFAULT 0,
                pending BOOLEAN DEFAULT 1,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
            )
            '''
        )

    @staticmethod
    def get(invite_id):
        """
        Gets all invites with a given id
        args: invite_id
        ret: invites
        """

        return database.fetch(
            'SELECT * FROM invites WHERE id = ? AND revoked = 0 AND PENDING = 1',
            (invite_id,)
        )

    @staticmethod
    def get_user_invites(user_id):
        """
        Gets all invites of a given user
        args: user_id
        ret: invites
        """

        return database.fetch(
            '''
            SELECT * FROM groups g
            LEFT JOIN invites i ON i.group_id = g.id
            WHERE i.user_id = ? AND i.revoked = 0 AND i.pending = 1
            ''',
            (user_id,)
        )

    @staticmethod
    def get_group_invites(group_id):
        """
        Gets all invites to a given group
        args: group_id
        ret: invites
        """

        return database.fetch(
            '''
            SELECT * FROM users u
            LEFT JOIN invites i ON i.user_id = u.id
            WHERE i.group_id = ? AND i.revoked = 0 AND i.pending = 1
            ''',
            (group_id,)
        )

    @staticmethod
    def create(user_id, group_id):
        """
        Creates an invite
        args: user_id, group_id
        ret: none
        """

        database.execute(
            'INSERT INTO invites (user_id, group_id) VALUES (?, ?)',
            (user_id, group_id)
        )

    @staticmethod
    def revoke(invite_id):
        """
        Revokes an invite
        args: invite_id
        ret: none
        """

        database.execute(
            'UPDATE invites SET revoked = 1 WHERE id = ?',
            (invite_id,)
        )

    @staticmethod
    def close(invite_id):
        """
        Closes an invite
        args: invite_id
        ret: none
        """

        database.execute(
            'UPDATE invites SET pending = 0 WHERE id = ?',
            (invite_id,)
        )