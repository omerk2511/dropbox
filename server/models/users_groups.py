from initialization import initializer
from ..handlers.database import database

class UsersGroups(object):
    @staticmethod
    @initializer
    def initialize():
        """
        Initializes the users_groups table
        args: none
        ret: none
        """

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
        """
        Creates a users_groups entry
        args: user_id, group_id
        ret: none
        """

        database.execute(
            'INSERT INTO users_groups(user_id, group_id) VALUES (?, ?)',
            (user_id, group_id)
        )

    @staticmethod
    def get_groups(user_id):
        """
        Gets all the groups of a given user
        args: user_id
        ret: groups
        """

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
        """
        Gets all the users of a given group
        args: group_id
        ret: users
        """

        return database.fetch(
            '''
            SELECT * FROM users u
            LEFT JOIN users_groups ug ON ug.user_id = u.id
            WHERE ug.group_id = ?
            ''',
            (group_id,)
        )

    @staticmethod
    def is_in_group(user_id, group_id):
        """
        Returns whether a given user in a member of a given group
        args: user_id, group_id
        ret: is_in_group
        """

        results = database.fetch(
            'SELECT * FROM users_groups WHERE user_id = ? AND group_id = ?',
            (user_id, group_id)
        )
        
        return True if results else False

    @staticmethod
    def delete(user_id, group_id):
        """
        Deletes a users_groups entry
        args: user_id, group_id
        ret: none
        """

        database.execute(
            'DELETE FROM users_groups WHERE user_id = ? AND group_id = ?',
            (user_id, group_id)
        )