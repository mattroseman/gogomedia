import os
from flask import Flask
from flask_cors import CORS
from database import db

from routes import add_routes


ENVIRONMENT = os.environ.get('ENVIRONMENT', 'local')

TEST_DB_HOST = os.environ.get('TEST_DB_HOST')
TEST_DB_PORT = os.environ.get('TEST_DB_PORT')
TEST_DB_USER = os.environ.get('TEST_DB_USER')
TEST_DB_PASS = os.environ.get('TEST_DB_PASS')
TEST_DB_NAME = os.environ.get('TEST_DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')


def create_app(test=False):
    app = Flask(__name__)
    CORS(app)

    # TODO user urandom to generate this
    app.secret_key = 'super secret key'

    if test:
        database_uri = f'postgresql://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}'
    else:
        database_uri = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = test
    app.config['LOGIN_DISABLED'] = test
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    add_routes(app)

    db.init_app(app)
    db.create_all(app=app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
