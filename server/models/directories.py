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
            WHERE u.id = ? AND d.`group` IS NULL
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
    def get_user_directory_tree(user_id):
        directories = Directories.get_user_directories(user_id)
        return Directories.get_directory_tree(directories)

    @staticmethod
    def get_group_directory_tree(group_id):
        directories = Directories.get_group_directories(group_id)
        return Directories.get_directory_tree(directories)

    @staticmethod
    def get_directory_tree(directories):
        root = [directory for directory in directories if directory[4] == None][0]
        directories = [directory for directory in directories if directory[4] != None]

        tree = {
            'id': root[0],
            'name': root[1],
            'owner': root[2],
            'type': 'directory',
            'files': []
        }

        while len(directories) != 0:
            parent = directories[0][4]
            parent_node = None

            tree_stack = [tree]

            while not parent_node and len(tree_stack) > 0:
                if tree_stack[0]['id'] == parent:
                    parent_node = tree_stack[0]
                else:
                    tree_stack += tree_stack[0]['files']
                    tree_stack = tree_stack[1:]

            if parent_node:
                parent_node['files'].append(
                    {
                        'id': directories[0][0],
                        'name': directories[0][1],
                        'owner': directories[0][2],
                        'type': 'directory',
                        'files': []
                    }
                )

            directories = directories[1:]

        return tree

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