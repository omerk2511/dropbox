from initialization import initializer
from ..handlers.database import database

class Groups(object):
    @staticmethod
    @initializer
    def initialize():
        database.execute(
            '''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name CHAR(255) NOT NULL,
                owner INTEGER,
                FOREIGN KEY(owner) REFERENCES users(id) ON DELETE CASCADE
            )
            '''
        )

    @staticmethod
    def create(name, owner):
        return database.execute(
            'INSERT INTO groups (name, owner) VALUES (?, ?)',
            (name, owner)
        )
    
    @staticmethod
    def update_name(group_id, name):
        database.execute(
            'UPDATE groups SET name = ? WHERE id = ?',
            (name, group_id)
        )

    @staticmethod
    def update_owner(group_id, owner):
        database.execute(
            'UPDATE groups SET owner = ? WHERE id = ?',
            (owner, group_id)
        )

    @staticmethod
    def delete(group_id):
        database.execute(
            'DELETE FROM groups WHERE id = ?',
            (group_id)
        )