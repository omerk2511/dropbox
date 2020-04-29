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
    def create(username, full_name, password):
        database.execute(
            'INSERT INTO users (username, full_name, password) VALUES (?, ?, ?)',
            (username, full_name, hashlib.sha256(password).hexdigest())
        )

    @staticmethod
    def log_in(username, password):
        users = database.fetch(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, hashlib.sha256(password).hexdigest())
        )

        if users:
            return jwt.encode({
                'id': users[0][0],
                'username': users[0][1],
                'full_name': users[0][2]
            }, JWT_SECRET_KEY, algorithm='HS256')
        
        return None