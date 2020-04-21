import json
import unittest
from base_test_case import GoGoMediaBaseTestCase

from database import db

from models.user import User
from models.media import Media


class GoGoMediaMediaViewsTestCase(GoGoMediaBaseTestCase):
    def test_nonexistent_user_media_endpoint(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'user doesn\'t exist')

    def test_add_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
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

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'not started')
        self.assertEqual(media.description, '')

    def test_add_media_missing_request_name_and_id_params(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'missing parameter \'name\' or parameter \'id\'')

    def test_add_media_mistyped_request_id_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'id': '12'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'id parameter must be type integer')

    def test_add_media_mistyped_request_name_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 23}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'name parameter must be type string')

    def test_add_media_mistyped_request_consumed_state_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed_state': True}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'consumed_state parameter must be \'not started\', \'started\', or \'finished\'')

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed_state': 'finised'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'consumed_state parameter must be \'not started\', \'started\', or \'finished\'')

    def test_add_media_mistyped_request_medium_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'medium': 'aduio'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'medium parameter must be \'film\', \'audio\', \'literature\', or \'other\'')

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'medium': 12}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'medium parameter must be \'film\', \'audio\', \'literature\', or \'other\'')

    def test_add_media_mistyped_request_description_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'description': 34}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'description parameter must be type string')

    def test_add_media_mistyped_request_order_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'order': '23'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'order parameter must be type integer')

    def test_add_media_not_started(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed_state': 'not started'}),
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

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'not started')

    def test_add_media_started(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed_state': 'started'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'started',
            'description': '',
            'order': 0
        })

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'started')

    def test_add_media_finished(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed_state': 'finished'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'finished',
            'description': '',
            'order': 0
        })

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'other')
        self.assertEqual(media.consumed_state, 'finished')

    def test_add_media_with_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'medium': 'film'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'film',
            'consumed_state': 'not started',
            'description': '',
            'order': 0
        })

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'film')
        self.assertEqual(media.consumed_state, 'not started')

    def test_add_media_with_medium_and_consumed_state(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({
                                       'name': 'testmedianame',
                                       'medium': 'audio',
                                       'consumed_state': 'started'
                                   }),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'audio',
            'consumed_state': 'started',
            'description': '',
            'order': 0
        })

        media = Media.query.filter_by(id=1).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertEqual(media.medium, 'audio')
        self.assertEqual(media.consumed_state, 'started')

    def test_add_media_with_description(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({
                                       'name': 'testmedianame',
                                       'description': 'some description'
                                   }),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'not started',
            'description': 'some description',
            'order': 0
        })

    def test_add_media_with_order(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({
                                       'name': 'testmedianame',
                                       'order': 654321
                                   }),
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
            'order': 654321
        })

    def test_add_multiple_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps([
                                       {'name': 'testmedianame1', 'description': 'hello world'},
                                       {'name': 'testmedianame2', 'medium': 'audio'},
                                       {'name': 'testmedianame3', 'order': 3}
                                   ]),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertListEqual(body['data'], [
            {
                'id': 1,
                'name': 'testmedianame1',
                'medium': 'other',
                'consumed_state': 'not started',
                'description': 'hello world',
                'order': 0
            },
            {
                'id': 2,
                'name': 'testmedianame2',
                'medium': 'audio',
                'consumed_state': 'not started',
                'description': '',
                'order': 0
            },
            {
                'id': 3,
                'name': 'testmedianame3',
                'medium': 'other',
                'consumed_state': 'not started',
                'description': '',
                'order': 3
            }
        ])

    def test_add_multiple_media_with_one_mistyped(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps([
                                       {'name': 'testmedianame1', 'description': 'something something'},
                                       {'name': 'testmedianame2', 'medium': 'film'},
                                       {'name': 'testmedianame3', 'description': 23}
                                   ]),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'description parameter must be type string')

        media_list = Media.query.all()

        self.assertListEqual(media_list, [])

    def test_update_media_consumed_state(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed_state='not started')
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'id': media.id, 'consumed_state': 'started'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'started',
            'description': '',
            'order': 0
        })

        media_list = Media.query.filter_by(medianame='testmedianame').all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertEqual(media_list[0].consumed_state, 'started')

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'id': media.id, 'consumed_state': 'finished'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'finished',
            'description': '',
            'order': 0
        })

        media_list = Media.query.filter_by(medianame='testmedianame').all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertEqual(media_list[0].consumed_state, 'finished')

    def test_update_media_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='film')
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'id': media.id, 'medium': 'literature'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'literature',
            'consumed_state': 'not started',
            'description': '',
            'order': 0
        })

        media_list = Media.query.filter_by(medianame='testmedianame').all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertEqual(media_list[0].medium, 'literature')

    def test_update_media_consumed_state_and_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({
                                       'id': media.id,
                                       'medium': 'audio',
                                       'consumed_state': 'finished'
                                   }),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'audio',
            'consumed_state': 'finished',
            'description': '',
            'order': 0
        })

        media_list = Media.query.filter_by(medianame='testmedianame').all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertEqual(media_list[0].consumed_state, 'finished')
        self.assertEqual(media_list[0].medium, 'audio')

    def test_update_media_description(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, description='some description')
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({
                                       'id': media.id,
                                       'description': 'some other description'
                                   }),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {
            'id': 1,
            'name': 'testmedianame',
            'medium': 'other',
            'consumed_state': 'not started',
            'description': 'some other description',
            'order': 0
        })

        media_list = Media.query.filter_by(medianame='testmedianame').all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertEqual(media_list[0].consumed_state, 'not started')
        self.assertEqual(media_list[0].medium, 'other')
        self.assertEqual(media_list[0].description, 'some other description')

    def test_update_media_order(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, order=9)
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({
                                       'id': media.id,
                                       'order': 88890
                                   }),
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
            'order': 88890
        })

        media_list = Media.query.filter_by(medianame='testmedianame').all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertEqual(media_list[0].order, 88890)

    def test_update_media_nonexistant_id(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'id': 1}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'logged in user doesn\'t have media with given id')

    def test_update_media_other_users_media_id(self):
        user1 = User('testname1', 'P@ssw0rd')
        user2 = User('testname2', 'pass123')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        media = Media('testmedianame', user1.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname2/media',
                                   data=json.dumps({'id': 1}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'logged in user doesn\'t have media with given id')

    def test_update_multiple_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id)
        media2 = Media('testmedianame2', user.id)
        media3 = Media('testmedianame3', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps([
                                       {'id': 1, 'description': 'hello world'},
                                       {'id': 2, 'medium': 'audio'},
                                       {'id': 3, 'order': 3}
                                   ]),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertListEqual(body['data'], [
            {
                'id': 1,
                'name': 'testmedianame1',
                'medium': 'other',
                'consumed_state': 'not started',
                'description': 'hello world',
                'order': 0
            },
            {
                'id': 2,
                'name': 'testmedianame2',
                'medium': 'audio',
                'consumed_state': 'not started',
                'description': '',
                'order': 0
            },
            {
                'id': 3,
                'name': 'testmedianame3',
                'medium': 'other',
                'consumed_state': 'not started',
                'description': '',
                'order': 3
            }
        ])

        media1_list = Media.query.filter_by(medianame='testmedianame1').all()
        media2_list = Media.query.filter_by(medianame='testmedianame2').all()
        media3_list = Media.query.filter_by(medianame='testmedianame3').all()

        self.assertEqual(len(media1_list), 1)
        self.assertEqual(len(media2_list), 1)
        self.assertEqual(len(media3_list), 1)
        self.assertEqual(media1_list[0].description, 'hello world')
        self.assertEqual(media2_list[0].medium, 'audio')
        self.assertEqual(media3_list[0].order, 3)

    def test_update_multiple_media_with_one_mistyped(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id)
        media2 = Media('testmedianame2', user.id)
        media3 = Media('testmedianame3', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps([
                                       {'id': 1, 'description': 'hello world'},
                                       {'id': 2, 'medium': 3},
                                       {'id': 3, 'order': 3}
                                   ]),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'medium parameter must be \'film\', \'audio\', \'literature\', or \'other\'')

        media1_list = Media.query.filter_by(medianame='testmedianame1').all()
        media2_list = Media.query.filter_by(medianame='testmedianame2').all()
        media3_list = Media.query.filter_by(medianame='testmedianame3').all()

        self.assertEqual(len(media1_list), 1)
        self.assertEqual(len(media2_list), 1)
        self.assertEqual(len(media3_list), 1)
        self.assertEqual(media1_list[0].description, '')
        self.assertEqual(media2_list[0].medium, 'other')
        self.assertEqual(media3_list[0].order, 0)

    def test_update_multiple_media_with_one_media_not_owned_by_user(self):
        user1 = User('testname1', 'P@ssw0rd')
        user2 = User('testname2', 'pass123')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        media1 = Media('testmedianame1', user2.id)
        media2 = Media('testmedianame2', user1.id)
        media3 = Media('testmedianame3', user2.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.commit()

        response = self.client.put('/user/testname2/media',
                                   data=json.dumps([
                                       {'id': 1, 'order': 2},
                                       # this media isn't owned by the testname2 user
                                       {'id': 2, 'description': 'something'},
                                       {'id': 3}
                                   ]),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 401)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'logged in user doesn\'t have media with given id')

        media1_list = Media.query.filter_by(medianame='testmedianame1').all()
        media2_list = Media.query.filter_by(medianame='testmedianame2').all()
        media3_list = Media.query.filter_by(medianame='testmedianame3').all()

        self.assertEqual(len(media1_list), 1)
        self.assertEqual(len(media2_list), 1)
        self.assertEqual(len(media3_list), 1)
        self.assertEqual(media1_list[0].order, 0)
        self.assertEqual(media2_list[0].description, '')
        self.assertEqual(media2_list[0].user, 1)

    def test_add_and_update_multiple_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id)
        media2 = Media('testmedianame2', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps([
                                       {'id': 1, 'order': 2},
                                       {'name': 'testmedianame3', 'description': 'some description'},
                                       {'name': 'testmedianame4'},
                                       {'id': 2, 'medium': 'film'}
                                   ]),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], [
            {
                'id': 1,
                'name': 'testmedianame1',
                'medium': 'other',
                'consumed_state': 'not started',
                'description': '',
                'order': 2
            },
            {
                'id': 3,
                'name': 'testmedianame3',
                'medium': 'other',
                'consumed_state': 'not started',
                'description': 'some description',
                'order': 0
            },
            {
                'id': 4,
                'name': 'testmedianame4',
                'medium': 'other',
                'consumed_state': 'not started',
                'description': '',
                'order': 0
            },
            {
                'id': 2,
                'name': 'testmedianame2',
                'medium': 'film',
                'consumed_state': 'not started',
                'description': '',
                'order': 0
            },
        ])

        media1_list = Media.query.filter_by(medianame='testmedianame1').all()
        media2_list = Media.query.filter_by(medianame='testmedianame2').all()
        media3_list = Media.query.filter_by(medianame='testmedianame3').all()
        media4_list = Media.query.filter_by(medianame='testmedianame4').all()

        self.assertEqual(len(media1_list), 1)
        self.assertEqual(len(media2_list), 1)
        self.assertEqual(len(media3_list), 1)
        self.assertEqual(len(media4_list), 1)
        self.assertEqual(media1_list[0].order, 2)
        self.assertEqual(media2_list[0].medium, 'film')

    def test_get_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, medium='film', consumed_state='started')
        media2 = Media('testmedianame2', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.commit()

        response = self.client.get('/user/testname/media')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertListEqual(sorted(body['data'], key=lambda media: media['name']),
                             [media1.as_dict(), media2.as_dict()])

    def test_get_media_with_specific_consumed_state(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed_state='started', medium='film')
        media2 = Media('testmedianame2', user.id, consumed_state='started')
        media3 = Media('testmedianame3', user.id, consumed_state='not started', medium='other')
        media4 = Media('testmedianame4', user.id, consumed_state='finished')
        media5 = Media('testmedianame5', user.id, consumed_state='not started', medium='audio')
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        response = self.client.get('/user/testname/media?consumed-state=not-started')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertListEqual(sorted(body['data'], key=lambda media: media['name']),
                             [media3.as_dict(), media5.as_dict()])

    def test_get_media_with_specific_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed_state='started', medium='film')
        media2 = Media('testmedianame2', user.id, medium='other')
        media3 = Media('testmedianame3', user.id, consumed_state='finished', medium='film')
        media4 = Media('testmedianame4', user.id, medium='film')
        media5 = Media('testmedianame5', user.id, consumed_state='not started')
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        response = self.client.get('/user/testname/media?medium=film')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(sorted(body['data'], key=lambda media: media['name']),
                         [media1.as_dict(), media3.as_dict(), media4.as_dict()])

    def test_get_media_with_specific_medium_and_specific_consumed_state(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed_state='finished', medium='film')
        media2 = Media('testmedianame2', user.id, medium='other')
        media3 = Media('testmedianame3', user.id, consumed_state='not started', medium='film')
        media4 = Media('testmedianame4', user.id, medium='film')
        media5 = Media('testmedianame5', user.id, consumed_state='started')
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        response = self.client.get('/user/testname/media?consumed-state=not-started&medium=film')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(sorted(body['data'], key=lambda media: media['name']),
                         [media3.as_dict(), media4.as_dict()])

    def test_get_media_with_malformed_consumed_state_url_parameter(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.get('/user/testname/media?consumed-state=true')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'consumed-state url parameter must be \'not-started\', \'started\',  or \'finished\'')

    def test_get_media_with_malformed_medium_url_parameter(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.get('/user/testname/media?medium=asdf')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'],
                         'medium url parameter must be \'film\', \'audio\', \'literature\', or \'other\'')

    def test_delete_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({'id': media.id}),
                                      content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])

        media_list = Media.query.filter(Media.user == user.id).all()

        self.assertEqual(media_list, [])

    def test_delete_media_missing_request_body_params(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({}),
                                      content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'missing parameter \'id\'')

    def test_delete_media_mistyped_request_body_param(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({'id': '12'}),
                                      content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 422)
        self.assertFalse(body['success'])
        self.assertEqual(body['message'], 'id parameter must be type integer')

    def test_delete_unexisting_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({'id': 3}),
                                      content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
