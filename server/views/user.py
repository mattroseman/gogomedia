from flask import request, jsonify, session
from database import db

from models.blacklisted_token import BlacklistedToken

from logic.user import add_user, get_user
from logic.login import login_required


def register():
    """
    register accepts POST request containing a field with new user information
    """
    body = request.get_json()

    if 'username' not in body:
        return jsonify({
            'success': False,
            'message': 'missing parameter \'username\''
        }), 422
    if 'password' not in body:
        return jsonify({
            'success': False,
            'message': 'missing parameter \'password\''
        }), 422

    username = body['username']
    password = body['password']

    # If this user exists already
    if get_user(username):
        return jsonify({
            'success': False,
            'message': 'username taken'
        }), 422

    user = add_user(username, password)

    auth_token = user.encode_auth_token()

    return jsonify({
        'success': True,
        'message': 'user successfully registered',
        'auth_token': auth_token
    }), 201


def login():
    """
    login accepts a POST request containing username and password, it then validates this information
    and logs in the user
    """
    body = request.get_json()

    if 'username' not in body:
        return jsonify({
            'success': False,
            'message': 'missing parameter \'username\''
        }), 422
    if 'password' not in body:
        return jsonify({
            'success': False,
            'message': 'missing parameter \'password\''
        }), 422

    username = body['username']
    password = body['password']

    user = get_user(username)

    if user:
        if user.authenticate_password(password):
            user.authenticated = True
            db.session.commit()

            auth_token = user.encode_auth_token()

            return jsonify({
                'success': True,
                'message': 'user successfully logged in',
                'auth_token': auth_token
            })
        else:
            return jsonify({
                'success': False,
                'message': 'incorrect password'
            }), 401

    return jsonify({
        'success': False,
        'message': 'user doesn\'t exist'
    }), 422


@login_required
def logout(logged_in_user):
    """
    logout logs the current user out
    """
    auth_token = request.headers.get('Authorization').split(' ')[1]
    blacklisted_token = BlacklistedToken(auth_token)
    db.session.add(blacklisted_token)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'user successfully logged out'
    })
