from initialization import initializer
from ..handlers.database import database

class Editors(object):
    @staticmethod
    @initializer
    def initialize():
        database.execute(
            '''
            CREATE TABLE IF NOT EXISTS editors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user INTEGER NOT NULL,
                file INTEGER,
                directory INTEGER,
                FOREIGN KEY(user) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(file) REFERENCES files(id) ON DELETE CASCADE,
                FOREIGN KEY(directory) REFERENCES directories(id) ON DELETE CASCADE
            )
            '''
        )

    @staticmethod
    def get(editor_id):
        return database.fetch(
            'SELECT * FROM editors WHERE id = ?',
            (editor_id,)
        )

    @staticmethod
    def get_file_editors(file_id):
        return database.fetch(
            'SELECT * FROM editors WHERE file = ?',
            (file_id,)
        )

    @staticmethod
    def get_directory_editors(directory_id):
        return database.fetch(
            'SELECT * FROM editors WHERE directory = ?',
            (directory_id,)
        )

    @staticmethod
    def is_file_editor(user_id, file_id):
        editors = database.fetch(
            'SELECT * FROM editors WHERE user = ? AND file = ?',
            (user_id, file_id)
        )

        return True if editors else False

    @staticmethod
    def is_directory_editor(user_id, directory_id):
        editors = database.fetch(
            'SELECT * FROM editors WHERE user = ? AND directory = ?',
            (user_id, directory_id)
        )

        return True if editors else False

    @staticmethod
    def create(user_id, file_id=None, directory_id=None):
        database.execute(
            'INSERT INTO editors(user, file, directory) VALUES (?, ?, ?)',
            (user_id, file_id, directory_id)
        )
    
    @staticmethod
    def delete(editor_id):
        database.execute(
            'DELETE FROM editors WHERE id = ?',
            (editor_id,)
        )