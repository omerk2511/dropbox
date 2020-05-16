from initialization import initializer
from files import Files
from ..handlers.database import database

class Directories(object):
    @staticmethod
    @initializer
    def initialize():
        """
        Initializes the directories table
        args: none
        ret: none
        """

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
        """
        Gets all directories with a given id
        args: directory_id
        ret: directories
        """

        return database.fetch(
            'SELECT * FROM directories WHERE id = ?',
            (directory_id,)
        )

    @staticmethod
    def get_sub_directories(parent):
        """
        Gets all the directories with a given parent
        args: parent
        ret: directories
        """

        return database.fetch(
            '''
            SELECT * FROM directories WHERE parent = ?
            ''',
            (parent,)
        )

    @staticmethod
    def get_user_directories(user_id):
        """
        Gets all the directories of a given user
        args: user_id
        ret: directories
        """

        return database.fetch(
            '''
            SELECT * FROM directories d
            LEFT JOIN users u ON d.owner = u.id
            WHERE u.id = ? AND d.`group` IS NULL
            ''',
            (user_id,)
        )

    @staticmethod
    def get_user_directories_under_parent(user_id, parent):
        """
        Gets all the directories of a given user under a given parent
        args: user_id, parent
        ret: directories
        """

        return database.fetch(
            '''
            SELECT * FROM directories d
            LEFT JOIN users u ON d.owner = u.id
            WHERE u.id = ? AND d.parent = ? AND d.`group` IS NULL
            ''',
            (user_id, parent)
        )

    @staticmethod
    def get_group_directories(group_id):
        """
        Gets all the directories in a given group
        args: group_id
        ret: directories
        """

        return database.fetch(
            '''
            SELECT * FROM directories d
            LEFT JOIN groups g ON d.`group` = g.id
            WHERE g.id = ?
            ''',
            (group_id,)
        )

    @staticmethod
    def get_group_directories_under_parent(group_id, parent):
        """
        Gets all the directories in a given group under a given parent
        args: group_id, parent
        ret: directories
        """

        return database.fetch(
            '''
            SELECT * FROM directories d
            LEFT JOIN groups g ON d.`group` = g.id
            WHERE g.id = ? AND d.parent = ?
            ''',
            (group_id, parent)
        )

    @staticmethod
    def get_user_directory_tree(user_id):
        """
        Returns the directory tree of a user
        args: user_id
        ret: directory_tree
        """

        directories = Directories.get_user_directories(user_id)
        return Directories.get_directory_tree(directories)

    @staticmethod
    def get_group_directory_tree(group_id):
        """
        Returns the directory tree of a group
        args: group_id
        ret: directory_tree
        """

        directories = Directories.get_group_directories(group_id)
        return Directories.get_directory_tree(directories)

    @staticmethod
    def get_directory_tree(directories):
        """
        Turns a directory list into a directory tree
        args: directories
        ret: directory_tree
        """

        root = [directory for directory in directories if directory[4] == None][0]
        directories = [directory for directory in directories if directory[4] != None]

        tree = {
            'id': root[0],
            'name': root[1],
            'owner': root[2],
            'type': 'directory',
            'files': [
                {
                    'id': f[0],
                    'name': f[2],
                    'owner': f[3],
                    'type': 'file'
                } for f in Files.get_directory_files(root[0])
            ]
        }

        while len(directories) != 0:
            parent = directories[0][4]
            parent_node = None

            tree_stack = [tree]

            while not parent_node and len(tree_stack) > 0:
                if tree_stack[0]['type'] == 'directory':
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
                        'files': [
                            {
                                'id': f[0],
                                'name': f[2],
                                'owner': f[3],
                                'type': 'file'
                            } for f in Files.get_directory_files(directories[0][0])
                        ]
                    }
                )

            directories = directories[1:]

        return tree

    @staticmethod
    def create(name, owner, group=None, parent=None):
        """
        Creates a directory
        args: name, owner, group, parent
        ret: created_directory_id
        """

        return database.execute(
            'INSERT INTO directories(name, owner, `group`, parent) VALUES (?, ?, ?, ?)',
            (name, owner, group, parent)
        )

    @staticmethod
    def update_owner_in_group(old_owner, new_owner, group):
        """
        Updates an owner in a group
        args: old_owner, new_owner, group
        ret: none
        """
        
        database.execute(
            'UPDATE directories SET owner = ? WHERE owner = ? AND `group` = ?',
            (new_owner, old_owner, group)
        )

    @staticmethod
    def update_name(directory_id, name):
        """
        Updates the name of a directory
        args: directory_id, name
        ret: none
        """

        database.execute(
            'UPDATE directories SET name = ? WHERE id = ?',
            (name, directory_id)
        )

    @staticmethod
    def update_owner(directory_id, owner):
        """
        Updates the owner of a directory
        args: directory_id, owner
        ret: none
        """

        database.execute(
            'UPDATE directories SET owner = ? WHERE id = ?',
            (owner, directory_id)
        )

    @staticmethod
    def update_parent(directory_id, parent):
        """
        Updates the parent of a directory
        args: directory_id, parent
        ret: none
        """

        database.execute(
            'UPDATE directories SET parent = ? WHERE id = ?',
            (parent, directory_id)
        )

    @staticmethod
    def delete(directory_id):
        """
        Deletes a directory
        args: directory_id
        ret: none
        """

        database.execute(
            'DELETE FROM directories WHERE id = ?',
            (directory_id,)
        )