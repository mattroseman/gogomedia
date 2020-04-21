from base_test_case import GoGoMediaBaseTestCase

from database import db

from models.user import User

from logic.user import add_user, get_user, get_user_by_id


class GoGoMediaUserLogicTestCase(GoGoMediaBaseTestCase):
    def test_add_user(self):
        add_user('testname', 'P@ssw0rd')

        user = User.query.filter(User.username == 'testname').first()

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testname')

    def test_get_user(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user, get_user('testname'))

    def test_get_user_by_id(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user, get_user_by_id(1))
