import pytest, json, sys, re, datetime
from bson.objectid import ObjectId
from bson.binary import Binary
from bson.json_util import loads, dumps
from flask import Flask
from flaskr import create_app
from flaskr.domain import mongo
from flask.testing import FlaskClient

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    testConfig = {
        'MONGO_URL': "mongodb://localhost:27017/",
        'MONGO_USERNAME':"user",
        'MONGO_PASSWORD':"pass",
        'MONGO_AUTH_SOURCE':"admin",
        'MONGO_DATABASE':"test_trakayo",
        'BASE_URL': "http:/127.0.0.1:666",
        'MAILING_SMTP_SERVER': "",
        'MAILING_SMTP_PORT': "",
        'MAILING_SENDER': "",
        'MAILING_SENDER_EMAIL': "",
        'MAILING_SMTP_PASSWORD': ""
    }
    app = create_app(testConfig)

    # create the database and load test data
    with app.app_context():
        initDB()

    yield app

def initDB():
    db = mongo.getDb()
    for collectionName in db.list_collection_names():
        db.drop_collection(collectionName)

    mongo.initDb()
    with open('tests/mongo.json') as json_file:
        data = loads(json_file.read())

        for collectionName, documents in data.items():
            db.get_collection(collectionName).insert_many(documents)

@pytest.fixture
def client(app: Flask):
    return app.test_client(use_cookies=False)

@pytest.fixture
def authHeader(client) -> dict:
    response = client.post(
        "/auth/login", json={"username": 'testuser', "password": 'pass'}
    )
    token = response.get_data( as_text = True )
    return {"Authorization" : "Bearer "+ token}


@pytest.fixture
def authHeaderAdmin(client) -> dict:
    response = client.post(
        "/auth/login", json={"username": 'testuseradmin', "password": 'pass'}
    )
    token = response.get_data( as_text = True )
    return {"Authorization" : "Bearer "+ token}
