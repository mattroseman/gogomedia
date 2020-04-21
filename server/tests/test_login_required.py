import jwt
import datetime
import json
from base_test_case import GoGoMediaBaseTestCase
from flask import current_app

from database import db

from models.user import User
from models.blacklisted_token import BlacklistedToken

from logic.media import get_media


class GoGoMediaLoginRequiredTestCase(GoGoMediaBaseTestCase):
    """
    These tests apply to any endpoint that has a login_required decorator on it. It is testing the decorator code,
    and not the specific endpoint itself. For testing purposes it uses /user/<username>/media.
    """
    def setUp(self):
        super()
        # login should be enabled for all these tests
        current_app.config['LOGIN_DISABLED'] = False

    def test_login_required_media_endpoint(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        # havn't logged in yet
        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'no authorization header')
        self.assertEqual(user.media, [])

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))
        auth_token = body['auth_token']

        # have logged in
        response = self.client.put('/user/testname/media',
                                   headers={'Authorization': 'JWT ' + auth_token},
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'not started',
            'description': '',
            'order': 0
        })

    def test_login_required_media_endpoint_malformed_authorization_header(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))
        auth_token = body['auth_token']

        response = self.client.put('/user/testname/media',
                                   headers={'Authorization': auth_token},
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'authorization header malformed')

    def test_login_required_media_endpoint_different_user(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        user1 = User('testname1', 'P@ssw0rd')
        user2 = User('testname2', 'pass123')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname1', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))
        auth_token = body['auth_token']

        self.assertIn('auth_token', body)

        response = self.client.put('/user/testname2/media',
                                   headers={'Authorization': 'JWT ' + auth_token},
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'not logged in as this user')

        media_list = get_media('testname2')
        self.assertEqual(media_list, [])

    def test_login_blacklisted_auth_token(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))
        auth_token = body['auth_token']

        blacklisted_token = BlacklistedToken(auth_token)
        db.session.add(blacklisted_token)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   headers={'Authorization': 'JWT ' + auth_token},
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'auth token blacklisted')

    def test_login_invalid_auth_token(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))
        auth_token = body['auth_token']
        # cut off the first character of the auth_token, making it invalid
        auth_token = auth_token[1:]

        response = self.client.put('/user/testname/media',
                                   headers={'Authorization': 'JWT ' + auth_token},
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'invalid token')

    def test_login_expired_auth_token(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        # Manually create an auth_token for user that is expired
        payload = {
            'exp': datetime.datetime.utcnow() - datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user.id
        }
        auth_token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

        response = self.client.put('/user/testname/media',
                                   headers={'Authorization': 'JWT ' + auth_token},
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'signature expired')
