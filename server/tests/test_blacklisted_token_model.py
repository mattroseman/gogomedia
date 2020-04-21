from base_test_case import GoGoMediaBaseTestCase

from database import db

from models.blacklisted_token import BlacklistedToken
from models.user import User


class GoGoMediaBlacklistedTokenModelTestCase(GoGoMediaBaseTestCase):
    def test_add_blacklisted_token(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        auth_token = user.encode_auth_token()

        blacklisted_token = BlacklistedToken(auth_token)
        db.session.add(blacklisted_token)
        db.session.commit()

        self.assertIn(blacklisted_token, db.session)
        self.assertEqual(blacklisted_token.id, 1)
        self.assertEqual(blacklisted_token.token, auth_token)

    def test_check_blacklist(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        auth_token = user.encode_auth_token()

        self.assertFalse(BlacklistedToken.check_blacklist(auth_token))

        blacklisted_token = BlacklistedToken(auth_token)
        db.session.add(blacklisted_token)
        db.session.commit()

        self.assertTrue(BlacklistedToken.check_blacklist(auth_token))
