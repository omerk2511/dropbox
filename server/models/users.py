import jwt
import hashlib

from initialization import initializer
from ..config import JWT_SECRET_KEY
from ..handlers.database import database

class Users(object):
    @staticmethod
    @initializer
    def initialize():
        """
        Initializes the users table
        args: none
        ret: none
        """

        database.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username CHAR(255) UNIQUE NOT NULL,
                full_name CHAR(255) NOT NULL,
                password CHAR(64) NOT NULL
            )
            '''
        )

    @staticmethod
    def get(user_id):
        """
        Gets all users with a given id
        args: user_id
        ret: users
        """

        return database.fetch(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        )

    @staticmethod
    def get_formatted(user_id):
        """
        Gets a formatted user entry
        args: user_id
        ret: formatted_user
        """

        user = database.fetch(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        )[0]

        return {
            'id': user[0],
            'username': user[1],
            'full_name': user[2]
        }

    @staticmethod
    def get_by_username(username):
        """
        Gets all users with a given username
        args: username
        ret: users
        """

        return database.fetch(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        )

    @staticmethod
    def create(username, full_name, password):
        """
        Creates a user
        args: username, full_name, password
        ret: user_id
        """

        return database.execute(
            'INSERT INTO users (username, full_name, password) VALUES (?, ?, ?)',
            (username, full_name, hashlib.sha256(password).hexdigest())
        )

    @staticmethod
    def update_full_name(user_id, full_name):
        """
        Updates the full_name of a given user
        args: user_id, full_name
        ret: none
        """

        database.execute(
            'UPDATE users SET full_name = ? WHERE id = ?',
            (full_name, user_id)
        )

    @staticmethod
    def update_password(user_id, password):
        """
        Updates the password of a given user
        args: user_id, password
        ret: none
        """

        database.execute(
            'UPDATE users SET password = ? WHERE id = ?',
            (hashlib.sha256(password).hexdigest(), user_id)
        )

    @staticmethod
    def log_in(username, password):
        """
        Logs a user in
        args: username, password
        ret: token
        """

        users = database.fetch(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, hashlib.sha256(password).hexdigest())
        )

        if users:
            return Users.get_jwt(users[0][0])
        
        return None

    @staticmethod
    def get_jwt(user_id):
        """
        Returns a JWT for a user
        args: user_id
        ret: token
        """

        users = database.fetch(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        )

        if users:
            return jwt.encode({
                'id': users[0][0],
                'username': users[0][1],
                'full_name': users[0][2]
            }, JWT_SECRET_KEY, algorithm='HS256')
        
        return None