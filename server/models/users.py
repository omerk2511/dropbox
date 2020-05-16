import jwt
import hashlib

from initialization import initializer
from ..config import JWT_SECRET_KEY
from ..handlers.database import database

class Users(object):
    @staticmethod
    @initializer
    def initialize():
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
        return database.fetch(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        )

    @staticmethod
    def get_formatted(user_id):
        user = database.fetch(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        )

        return {
            'id': user[0],
            'username': user[1],
            'full_name': user[2]
        }

    @staticmethod
    def get_by_username(username):
        return database.fetch(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        )

    @staticmethod
    def create(username, full_name, password):
        return database.execute(
            'INSERT INTO users (username, full_name, password) VALUES (?, ?, ?)',
            (username, full_name, hashlib.sha256(password).hexdigest())
        )

    @staticmethod
    def update_full_name(user_id, full_name):
        database.execute(
            'UPDATE users SET full_name = ? WHERE id = ?',
            (full_name, user_id)
        )

    @staticmethod
    def update_password(user_id, password):
        database.execute(
            'UPDATE users SET password = ? WHERE id = ?',
            (hashlib.sha256(password).hexdigest(), user_id)
        )

    @staticmethod
    def log_in(username, password):
        users = database.fetch(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, hashlib.sha256(password).hexdigest())
        )

        if users:
            return Users.get_jwt(users[0][0])
        
        return None

    @staticmethod
    def get_jwt(user_id):
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