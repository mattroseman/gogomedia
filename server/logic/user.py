from database import db
from models.user import User
import bcrypt


def add_user(username, password):
    """
    add_user takes a new user's information and adds it to the database
    @param username: a string representing the user's username
    @param password: a string representing the user's password
    @return: The newly created user
    """
    user = User(username, password)
    db.session.add(user)
    db.session.commit()

    return user


def get_user(username):
    """
    get_user queries the database for a user with the given username, returning the user instance
    """
    return User.query.filter_by(username=username).first()


def get_user_by_id(user_id):
    """
    get_user_by_id queries the database for a user with the given user id, returning the user instance
    """
    return User.query.filter_by(id=user_id).first()
