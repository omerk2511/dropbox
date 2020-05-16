from initialization import initializer
from ..handlers.database import database

class Editors(object):
    @staticmethod
    @initializer
    def initialize():
        """
        Initializes the editors table
        args: none
        ret: none
        """

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
        """
        Gets all editors with a given id
        args: editor_id
        ret: editors
        """

        return database.fetch(
            'SELECT * FROM editors WHERE id = ?',
            (editor_id,)
        )

    @staticmethod
    def get_file_editors(file_id):
        """
        Gets all the editors of a given file
        args: file_id
        ret: editors
        """

        return database.fetch(
            'SELECT * FROM editors WHERE file = ?',
            (file_id,)
        )

    @staticmethod
    def get_directory_editors(directory_id):
        """
        Gets all the editors of a given directory
        args: directory_id
        ret: editors
        """

        return database.fetch(
            'SELECT * FROM editors WHERE directory = ?',
            (directory_id,)
        )

    @staticmethod
    def is_file_editor(user_id, file_id):
        """
        Returns whether a given user is an editor of a given file
        args: user_id, file_id
        ret: is_editor
        """

        editors = database.fetch(
            'SELECT * FROM editors WHERE user = ? AND file = ?',
            (user_id, file_id)
        )

        return True if editors else False

    @staticmethod
    def is_directory_editor(user_id, directory_id):
        """
        Returns whether a given user is an editor of a given directory
        args: user_id, directory_id
        ret: is_editor
        """

        editors = database.fetch(
            'SELECT * FROM editors WHERE user = ? AND directory = ?',
            (user_id, directory_id)
        )

        return True if editors else False

    @staticmethod
    def create(user_id, file_id=None, directory_id=None):
        """
        Creates an editor
        args: user_id, file_id, directory_id
        ret: none
        """

        database.execute(
            'INSERT INTO editors(user, file, directory) VALUES (?, ?, ?)',
            (user_id, file_id, directory_id)
        )
    
    @staticmethod
    def delete(editor_id):
        """
        Deletes an editor
        args: editor_id
        ret: none
        """

        database.execute(
            'DELETE FROM editors WHERE id = ?',
            (editor_id,)
        )