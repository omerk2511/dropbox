import uuid

from initialization import initializer
from ..handlers.database import database

class Files(object):
    @staticmethod
    @initializer
    def initialize():
        database.execute(
            '''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid CHAR(36) NOT NULL,
                name CHAR(255) NOT NULL,
                owner INTEGER NOT NULL,
                directory INTEGER NOT NULL,
                FOREIGN KEY(owner) REFERENCES users(id),
                FOREIGN KEY(directory) REFERENCES directories(id) ON DELETE CASCADE
            )
            '''
        )

    @staticmethod
    def get(file_id):
        return database.fetch(
            'SELECT * FROM files WHERE id = ?',
            (file_id,)
        )

    @staticmethod
    def create(name, owner, directory):
        file_uuid = str(uuid.uuid4())

        return {
            'id': database.execute(
                'INSERT INTO files (uuid, name, owner, directory) VALUES (?, ?, ?, ?)',
                (name, owner, directory)
            ),
            'uuid': file_uuid
        }

    @staticmethod
    def update_name(file_id, name):
        database.execute(
            'UPDATE files SET name = ? WHERE id = ?',
            (name, file_id)
        )

    @staticmethod
    def update_owner(file_id, owner):
        database.execute(
            'UPDATE files SET owner = ? WHERE id = ?',
            (owner, file_id)
        )

    @staticmethod
    def update_directory(file_id, directory):
        database.execute(
            'UPDATE files SET directory = ? WHERE id = ?',
            (directory, file_id)
        )