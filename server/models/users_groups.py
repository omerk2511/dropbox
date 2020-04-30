from initialization import initializer
from ..handlers.database import database

class UsersGroups(object):
    @staticmethod
    @initializer
    def initialize():
        database.execute(
            '''
            CREATE TABLE IF NOT EXISTS users_groups (
                user_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                PRIMARY KEY(user_id, group_id),
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
            )
            '''
        )

    @staticmethod
    def insert(user_id, group_id):
        database.execute(
            'INSERT INTO users_groups(user_id, group_id) VALUES (?, ?)',
            (user_id, group_id)
        )

    @staticmethod
    def get_groups(user_id):
        return database.fetch(
            '''
            SELECT * FROM groups g
            LEFT JOIN users_groups ug ON ug.group_id = g.id
            WHERE ug.user_id = ?
            ''',
            (user_id,)
        )

    @staticmethod
    def get_users(group_id):
        return database.fetch(
            '''
            SELECT * FROM users u
            LEFT JOIN users_groups ug ON ug.user_id = u.id
            WHERE ug.group_id = ?
            ''',
            (group_id,)
        )

    @staticmethod
    def delete(user_id, group_id):
        database.execute(
            'DELETE FROM users_groups WHERE user_id = ? AND group_id = ?',
            (user_id, group_id)
        )