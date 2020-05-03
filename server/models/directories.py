from initialization import initializer
from ..handlers.database import database

class Directories(object):
    @staticmethod
    @initializer
    def initialize():
        database.execute(
            '''
            CREATE TABLE IF NOT EXISTS directories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name CHAR(255) NOT NULL,
                owner INTEGER NOT NULL,
                `group` INTEGER,
                parent INTEGER,
                FOREIGN KEY(owner) REFERENCES users(id),
                FOREIGN KEY(`group`) REFERENCES groups(id) ON DELETE CASCADE,
                FOREIGN KEY(parent) REFERENCES directories(id) ON DELETE CASCADE
            )
            '''
        )

    @staticmethod
    def get(directory_id):
        return database.fetch(
            'SELECT * FROM directories WHERE id = ?',
            (directory_id,)
        )

    @staticmethod
    def get_user_directories(user_id):
        return database.fetch(
            '''
            SELECT * FROM directories d
            LEFT JOIN users u ON d.owner = u.id
            WHERE u.id = ? AND d.`group` = NULL
            ''',
            (user_id,)
        )

    @staticmethod
    def get_group_directories(group_id):
        return database.fetch(
            '''
            SELECT * FROM directories d
            LEFT JOIN groups g ON d.`group` = g.id
            WHERE g.id = ?
            ''',
            (group_id,)
        )

    @staticmethod
    def create(name, owner, group=None, parent=None):
        return database.execute(
            'INSERT INTO directories(name, owner, `group`, parent) VALUES (?, ?, ?, ?)',
            (name, owner, group, parent)
        )

    @staticmethod
    def delete(directory_id):
        database.execute(
            'DELETE FROM directories WHERE id = ?',
            (directory_id,)
        )