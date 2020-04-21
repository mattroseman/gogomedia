from database import db
from flask import current_app
import bcrypt
import jwt
import datetime

from models.blacklisted_token import BlacklistedToken


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True, nullable=False)
    passhash = db.Column('passhash', db.String(60))
    media = db.relationship('Media', backref='users', lazy=True)

    def __init__(self, username, password):
        self.username = username
        password = password.encode('utf-8')
        self.passhash = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    def __repr__(self):
        return '<User(id={}, username={}, passhash={})>'.format(
            self.id, self.username, self.passhash)

    def authenticate_password(self, password):
        """
        authenticate_password takes an unhashed password, and returns True if this mathces the
        hashed password + salt for this user
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.passhash.encode('utf-8'))

    def encode_auth_token(self):
        """
        get_auth_token generates a new auth token with this user's id
        @return: a string representing the auth token to use
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=5),
            'iat': datetime.datetime.utcnow(),
            'sub': self.id
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def decode_auth_token(auth_token):
        """
        decode_auth_token is a static method that takes some user's auth token, deocdes it, and returns the user's id
        @param auth_token: a string representing the encrypted auth token made for some user
        @return: a number representing the user's id that was used when this auth token was encrypted, or a string
            representing an error message if auth token decoding failed.
        """
        if BlacklistedToken.check_blacklist(auth_token):
            return 'auth token blacklisted'

        try:
            payload = jwt.decode(auth_token, current_app.config['SECRET_KEY'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'signature expired'
        except jwt.InvalidTokenError:
            return 'invalid token'
