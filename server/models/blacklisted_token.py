import datetime

from database import db


class BlacklistedToken(db.Model):
    __tablename__ = 'blacklisted_tokens'
    id = db.Column('id', db.Integer, primary_key=True)
    token = db.Column('token', db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column('blacklisted_on', db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<BlacklistedToken(id={}, token={}, blacklisted_on={})>'.format(
            self.id, self.token, self.blacklisted_on)

    @staticmethod
    def check_blacklist(auth_token):
        """
        check_blacklist takes an auth token and checks the blacklisted_tokens table to see
        if this auth token has been blacklisted.
        @param auth_token: a string representing an auth token
        @return: a boolean that is True if this token has been blacklisted, and False otherwise
        """
        return BlacklistedToken.query.filter_by(token=auth_token).first() is not None
