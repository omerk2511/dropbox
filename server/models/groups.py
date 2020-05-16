from initialization import initializer
from ..handlers.database import database

class Groups(object):
    @staticmethod
    @initializer
    def initialize():
        """
        Initializes the groups table
        args: none
        ret: none
        """

        database.execute(
            '''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name CHAR(255) NOT NULL,
                owner INTEGER NOT NULL,
                FOREIGN KEY(owner) REFERENCES users(id) ON DELETE CASCADE
            )
            '''
        )

    @staticmethod
    def get(group_id):
        """
        Gets all groups with a given id
        args: group_id
        ret: groups
        """

        return database.fetch(
            'SELECT * FROM groups WHERE id = ?',
            (group_id,)
        )

    @staticmethod
    def create(name, owner):
        """
        Creates a group
        args: name, owner
        ret: group_id
        """

        return database.execute(
            'INSERT INTO groups (name, owner) VALUES (?, ?)',
            (name, owner)
        )
    
    @staticmethod
    def update_name(group_id, name):
        """
        Updates a group name
        args: group_id, name
        ret: none
        """

        database.execute(
            'UPDATE groups SET name = ? WHERE id = ?',
            (name, group_id)
        )

    @staticmethod
    def update_owner(group_id, owner):
        """
        Updates a group owner
        args: group_id, owner
        ret: none
        """

        database.execute(
            'UPDATE groups SET owner = ? WHERE id = ?',
            (owner, group_id)
        )

    @staticmethod
    def delete(group_id):
        """
        Delets a group
        args: group_id
        ret: none
        """

        database.execute(
            'DELETE FROM groups WHERE id = ?',
            (group_id,)
        )