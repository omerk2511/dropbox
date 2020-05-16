import base64
import os
from uuid import uuid4

from initialization import initializer
from ..handlers.database import database
from ..config import FILES_PATH

class Files(object):
    @staticmethod
    @initializer
    def initialize():
        """
        Initializes the files table
        args: none
        ret: none
        """

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
        """
        Returns all the files with a given id
        args: file_id
        ret: files
        """

        return database.fetch(
            'SELECT * FROM files WHERE id = ?',
            (file_id,)
        )

    @staticmethod
    def get_directory_files(directory_id):
        """
        Returns all the files under a given directory
        args: directory_id
        ret: files
        """

        return database.fetch(
            'SELECT * FROM files WHERE directory = ?',
            (directory_id,)
        )

    @staticmethod
    def create(name, owner, directory):
        """
        Creates a file
        args: name, owner, directory
        ret: file_id
        """

        file_uuid = str(uuid4())

        with open(FILES_PATH + file_uuid, 'wb+') as f:
            f.write('')

        return database.execute(
            'INSERT INTO files (uuid, name, owner, directory) VALUES (?, ?, ?, ?)',
            (file_uuid, name, owner, directory)
        )

    @staticmethod
    def write(file_id, content):
        """
        Writes content into a given file
        args: file_id, content
        ret: none
        """

        file_uuid = Files.get(file_id)[0][1]

        with open(FILES_PATH + file_uuid, 'wb+') as f:
            f.write(base64.b64decode(content))

    @staticmethod
    def read(file_id):
        """
        Reads content from a given file
        args: file_id
        ret: content
        """

        file_uuid = Files.get(file_id)[0][1]

        with open(FILES_PATH + file_uuid, 'rb+') as f:
            return base64.b64encode(f.read())

    @staticmethod
    def update_name(file_id, name):
        """
        Updates the name of a given file
        args: file_id, name
        ret: none
        """

        database.execute(
            'UPDATE files SET name = ? WHERE id = ?',
            (name, file_id)
        )

    @staticmethod
    def update_owner(file_id, owner):
        """
        Updates the owner of a given file
        args: file_id, owner
        ret: none
        """

        database.execute(
            'UPDATE files SET owner = ? WHERE id = ?',
            (owner, file_id)
        )

    @staticmethod
    def update_directory(file_id, directory):
        """
        Updates the directory of a given file
        args: file_id, directory
        ret: none
        """

        database.execute(
            'UPDATE files SET directory = ? WHERE id = ?',
            (directory, file_id)
        )

    @staticmethod
    def delete(file_id):
        """
        Deletes a file
        args: file_id
        ret: none
        """

        file_uuid = Files.get(file_id)[0][1]
        os.remove(FILES_PATH + file_uuid)

        database.execute(
            'DELETE FROM files WHERE id = ?',
            (file_id,)
        )