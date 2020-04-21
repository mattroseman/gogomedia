from flask_testing import TestCase
from flask import current_app

from app import create_app
from database import db


class GoGoMediaBaseTestCase(TestCase):

    def create_app(self):
        return create_app(test=True)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
