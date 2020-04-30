from initialization import initializer
from ..handlers.database import database

class Invites(object):
    @staticmethod
    @initializer
    def initialize():
        database.execute(
            '''
            CREATE TABLE IF NOT EXISTS invites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user INTEGER NOT NULL,
                group INTEGER NOT NULL,
                revoked BOOLEAN DEFAULT 0,
                pending BOOLEAN DEFAULT 1,
                FOREIGN KEY(user) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(group) REFERENCES groups(id) ON DELETE CASCADE
            )
            '''
        )

    @staticmethod
    def get(invite_id):
        return database.fetch(
            'SELECT * FROM invites WHERE id = ?',
            (invite_id,)
        )

    @staticmethod
    def get_user_invites(user_id):
        return database.fetch(
            '''
            SELECT * FROM groups g
            LEFT JOIN invites i ON i.group = g.id
            WHERE i.user = ?
            ''',
            (user_id,)
        )

    @staticmethod
    def get_group_invites(group_id):
        return database.fetch(
            '''
            SELECT * FROM users u
            LEFT JOIN invites i ON i.user = u.id
            WHERE i.group = ?
            ''',
            (group_id,)
        )

    @staticmethod
    def create(user, group):
        database.execute(
            'INSERT INTO invites (user, group) VALUES (?, ?)',
            (user, group)
        )

    @staticmethod
    def revoke(invite_id):
        database.execute(
            'UPDATE invites SET revoked = 1 WHERE id = ?',
            (invite_id,)
        )

    @staticmethod
    def close(invite_id):
        database.execute(
            'UPDATE invites SET pending = 0 WHERE id = ?',
            (invite_id,)
        )