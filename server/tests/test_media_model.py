from base_test_case import GoGoMediaBaseTestCase
from sqlalchemy.exc import StatementError

from database import db

from models.user import User
from models.media import Media, mediums, consumed_states


class GoGoMediaMediaModelTestCase(GoGoMediaBaseTestCase):
    def test_construct_media_with_invalid_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        with self.assertRaises(ValueError) as e:
            media = Media('testmedianame', user.id, medium='asdf')

        self.assertEqual(str(e.exception),
                         'medium must be one of these values: {}'.format(mediums))

    def test_construct_media_with_invalid_consumed_state(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        with self.assertRaises(ValueError) as e:
            media = Media('testmedianame', user.id, consumed_state='asdf')

        self.assertEqual(str(e.exception),
                         'consumed_state must be on of these values: {}'.format(consumed_states))

    def test_add_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'not started')
        self.assertEqual(media.description, '')
        self.assertEqual(media.order, 0)

    def test_add_not_started_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed_state='not started')
        db.session.add(media)
        db.session.commit()

        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'not started')
        self.assertEqual(media.order, 0)

    def test_add_started_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed_state='started')
        db.session.add(media)
        db.session.commit()

        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'started')
        self.assertEqual(media.order, 0)

    def test_add_finished_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed_state='finished')
        db.session.add(media)
        db.session.commit()

        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'finished')
        self.assertEqual(media.order, 0)

    def test_add_media_with_medium_type_film(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='film')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'film')

    def test_add_media_with_medium_type_audio(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='audio')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'audio')

    def test_add_media_with_medium_type_literature(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='literature')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'literature')

    def test_add_media_with_medium_type_other(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='other')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'other')

    def test_add_media_with_description(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, description='some description')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.description, 'some description')

    def test_add_media_with_specific_order(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, order=23)
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.order, 23)

    def test_update_media_consumed_state(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.consumed_state, 'not started')

        media.consumed_state = 'finished'
        db.session.commit()

        self.assertEqual(media.consumed_state, 'finished')

    def test_update_media_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='literature')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'literature')

        media.medium = 'audio'
        db.session.commit()

        self.assertEqual(media.medium, 'audio')

    def test_update_media_description(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, description='asdf')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.description, 'asdf')

        media.description = 'some description'
        db.session.commit()

        self.assertEqual(media.description, 'some description')

    def test_update_media_order(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, order=2)
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.order, 2)

        media.order = 34
        db.session.commit()

        self.assertEqual(media.order, 34)

    def test_remove_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertTrue(media in db.session)

        db.session.delete(media)
        db.session.commit()

        self.assertFalse(media in db.session)

    def test_as_dict(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame',
                      user.id,
                      medium='literature',
                      consumed_state='started',
                      description='some description',
                      order=5)
        db.session.add(media)
        db.session.commit()

        self.assertDictEqual(media.as_dict(), {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'literature',
            'consumed_state': 'started',
            'description': 'some description',
            'order': 5
        })
