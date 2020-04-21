import datetime
import jwt
from flask import current_app

from base_test_case import GoGoMediaBaseTestCase

from database import db

from models.user import User


class GoGoMediaUserModelTestCase(GoGoMediaBaseTestCase):
    def test_add_user(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user in db.session)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, 'testname')

    def test_remove_user(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user in db.session)

        db.session.delete(user)
        db.session.commit()

        self.assertFalse(user in db.session)

    def test_user_authenticate_password(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertFalse(user.authenticate_password('pass123'))
        self.assertTrue(user.authenticate_password('P@ssw0rd'))

    def test_user_encode_auth_token(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        auth_token = user.encode_auth_token()

        self.assertIsInstance(auth_token, str)

    def test_user_decode_auth_token(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        auth_token = user.encode_auth_token()

        user_id = User.decode_auth_token(auth_token)

        self.assertIsInstance(user_id, int)
        self.assertEqual(user_id, 1)

    def test_user_decode_auth_token_invalid(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        auth_token = user.encode_auth_token()
        # remove first character to make auth_token invalid
        auth_token = auth_token[1:]

        user_id = User.decode_auth_token(auth_token)

        self.assertIsInstance(user_id, str)
        self.assertEqual(user_id, 'invalid token')

    def test_user_decode_auth_token_expired(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        # manually create expired auth_token
        payload = {
            'exp': datetime.datetime.utcnow() - datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user.id
        }
        auth_token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256').decode()

        user_id = User.decode_auth_token(auth_token)

        self.assertIsInstance(user_id, str)
        self.assertEqual(user_id, 'signature expired')
