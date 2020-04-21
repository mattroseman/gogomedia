from base_test_case import GoGoMediaBaseTestCase

from database import db

from models.user import User
from models.media import Media

from logic.media import add_media, update_media, remove_media, get_media, get_media_by_id


class GoGoMediaMediaLogicTestCase(GoGoMediaBaseTestCase):
    def test_add_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = add_media(user.id, 'testmedianame')

        self.assertIsNotNone(media)
        self.assertIn(media, db.session)
        self.assertEqual(media.id, 1)
        self.assertEqual(media.user, 1)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'not started')
        self.assertEqual(media.description, '')
        self.assertEqual(media.order, 0)

    def test_add_media_with_consumed_state_argument(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = add_media(user.id, 'testmedianame', consumed_state='finished')

        self.assertIsNotNone(media)
        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'finished')

    def test_add_media_with_medium_argument(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = add_media(user.id, 'testmedianame', medium='audio')

        self.assertIsNotNone(media)
        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.medium, 'audio')
        self.assertEqual(media.consumed_state, 'not started')

    def test_add_media_with_description_argument(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = add_media(user.id, 'testmedianame', description='some description')

        self.assertIsNotNone(media)
        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'not started')
        self.assertEqual(media.description, 'some description')

    def test_add_media_with_order_argument(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = add_media(user.id, 'testmedianame', order=444)

        self.assertIsNotNone(media)
        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.order, 444)

    def test_update_media_consumed_state_property(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.consumed_state, 'not started')
        self.assertEqual(media.medium, 'other')

        returned_media = update_media(media.id, consumed_state='started')

        self.assertEqual(returned_media, media)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'started')

        returned_media = update_media(media.id, consumed_state='finished')

        self.assertEqual(returned_media, media)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'finished')

    def test_update_media_medium_property(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'other')

        returned_media = update_media(media.id, medium='film')

        self.assertEqual(returned_media, media)
        self.assertEqual(media.medium, 'film')
        self.assertEqual(media.consumed_state, 'not started')

        returned_media = update_media(media.id, medium='audio')

        self.assertEqual(returned_media, media)
        self.assertEqual(media.medium, 'audio')
        self.assertEqual(media.consumed_state, 'not started')

    def test_update_media_medianame_property(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medianame, 'testmedianame')

        returned_media = update_media(media.id, medianame='testchangedmedianame')

        self.assertEqual(returned_media, media)
        self.assertEqual(media.medianame, 'testchangedmedianame')
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'not started')

    def test_update_media_description_property(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.description, '')

        returned_media = update_media(media.id, description='some description')

        self.assertEqual(returned_media, media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'not started')
        self.assertEqual(media.description, 'some description')

    def test_update_media_order_property(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.order, 0)

        returned_media = update_media(media.id, order=52)

        self.assertEqual(returned_media, media)
        self.assertEqual(media.order, 52)

    def test_update_media_no_change(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame',
                      user.id,
                      medium='film',
                      consumed_state='finished',
                      description='some description',
                      order=12345)
        db.session.add(media)
        db.session.commit()

        returned_media = update_media(media.id)

        self.assertEqual(returned_media, media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.medium, 'film')
        self.assertEqual(media.consumed_state, 'finished')
        self.assertEqual(media.description, 'some description')
        self.assertEqual(media.order, 12345)

    def test_remove_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertIn(media, db.session)

        remove_media(media.id)

        self.assertFalse(media in db.session)

    def test_get_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        media_list = sorted(get_media('testname'), key=lambda media: media.medianame)

        self.assertEqual(media_list, [media])

    def test_get_media_multiple_elements(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id)
        media2 = Media('testmedianame2', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.commit()

        media_list = sorted(get_media('testname'), key=lambda media: media.medianame)

        self.assertListEqual(media_list, [media1, media2])

    def test_get_media_multiple_users(self):
        """
        'testname1': ['testmedianame1', 'testmedianame2', 'testmedianame3']
        'testname2': ['testmedianame4', 'testmedianame1']
        """
        user1 = User('testname1', 'P@ssw0rd')
        user2 = User('testname2', 'P@ssw0rd')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        media1 = Media('testmedianame1', user1.id)
        media2 = Media('testmedianame2', user1.id)
        media3 = Media('testmedianame3', user1.id)
        media4 = Media('testmedianame4', user2.id)
        media5 = Media('testmedianame1', user2.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        user1_media_list = sorted(get_media('testname1'), key=lambda media: media.medianame)

        self.assertListEqual(user1_media_list, [media1, media2, media3])

        user2_media_list = sorted(get_media('testname2'), key=lambda media: media.medianame)

        self.assertListEqual(user2_media_list, [media5, media4])

    def test_get_media_list_filtered_by_consumed_state(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed_state='finished')
        media2 = Media('testmedianame2', user.id, consumed_state='not started')
        media3 = Media('testmedianame3', user.id, consumed_state='started')
        media4 = Media('testmedianame4', user.id, consumed_state='finished')
        media5 = Media('testmedianame5', user.id, consumed_state='started')
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        not_started_media_list = sorted(get_media('testname', consumed_state='not started'),
                                        key=lambda media: media.medianame)
        started_media_list = sorted(get_media('testname', consumed_state='started'),
                                    key=lambda media: media.medianame)
        finished_media_list = sorted(get_media('testname', consumed_state='finished'),
                                     key=lambda media: media.medianame)

        self.assertListEqual(not_started_media_list, [media2])
        self.assertListEqual(started_media_list, [media3, media5])
        self.assertListEqual(finished_media_list, [media1, media4])

    def test_get_media_with_specific_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, medium='other', consumed_state='not started')
        media2 = Media('testmedianame2', user.id, medium='film', consumed_state='finished')
        media3 = Media('testmedianame3', user.id, medium='literature')
        media4 = Media('testmedianame4', user.id, medium='audio', consumed_state='not started')
        media5 = Media('testmedianame5', user.id, medium='film', consumed_state='started')
        media6 = Media('testmedianame6', user.id, medium='film', consumed_state='finished')
        media7 = Media('testmedianame7', user.id, medium='audio')
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.add(media6)
        db.session.add(media7)
        db.session.commit()

        other_media_list = sorted(get_media('testname', medium='other'),
                                  key=lambda media: media.medianame)
        film_media_list = sorted(get_media('testname', medium='film'),
                                 key=lambda media: media.medianame)
        audio_media_list = sorted(get_media('testname', medium='audio'),
                                  key=lambda media: media.medianame)
        literature_media_list = sorted(get_media('testname', medium='literature'),
                                       key=lambda media: media.medianame)

        self.assertListEqual(other_media_list, [media1])
        self.assertListEqual(film_media_list, [media2, media5, media6])
        self.assertListEqual(audio_media_list, [media4, media7])
        self.assertListEqual(literature_media_list, [media3])

    def test_get_media_empty_list(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        empty_media_list = get_media('testname')
        empty_not_started_media_list = get_media('testname', consumed_state='not started')
        empty_started_media_list = get_media('testname', consumed_state='started')
        empty_finished_media_list = get_media('testname', consumed_state='finished')

        self.assertListEqual(empty_media_list, [])
        self.assertListEqual(empty_not_started_media_list, [])
        self.assertEqual(empty_started_media_list, [])
        self.assertEqual(empty_finished_media_list, [])

    def test_get_media_by_id(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        returned_media = get_media_by_id(media.id)

        self.assertEqual(returned_media, media)
        self.assertEqual(returned_media.id, media.id)
        self.assertEqual(returned_media.medianame, media.medianame)
