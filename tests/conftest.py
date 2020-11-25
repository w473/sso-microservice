import pytest, json, sys, re, datetime
from bson.objectid import ObjectId
from bson.binary import Binary
from bson.json_util import loads, dumps
from flask import Flask
from flaskr import create_app
from flaskr.domain import mongo

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
        'MAILING_SMTP_SERVER': "ittravel.atthost24.pl",
        'MAILING_SMTP_PORT': "587",
        'MAILING_SENDER': "TRAKAYO",
        'MAILING_SENDER_EMAIL': "contact@ittravel.eu",
        'MAILING_SMTP_PASSWORD': "potato"
    }
    app = create_app(testConfig)

    # create the database and load test data
    with app.app_context():
        initDB()
        # get_db().executescript(_data_sql)

    yield app

    # # close and remove the temporary database
    # os.close(db_fd)
    # os.unlink(db_path)

def initDB():
    db = mongo.getDb()
    for collectionName in db.list_collection_names():
        db.drop_collection(collectionName)

    # isObjectId = re.compile('^ObjectId\("[a-z0-9]*"\)$')
    # isISODate = re.compile('/^ISODate("[0-9\\-:]Z")$/')

    with open('tests/mongo.json') as json_file:
        data = loads(json_file.read())
        # print(data)

        for collectionName, documents in data.items():
            # newDocumentList = [];            
            # for document in documents:
            #     for fieldName, fieldValue in document.items():
            #         if isinstance(fieldValue, str):
            #             if re.match(r'^ObjectId\("[a-z0-9]*"\)$', fieldValue):
            #                 fieldValue = ObjectId(fieldValue.replace('ObjectId("', '').replace('")', ''));
            #             elif re.match(r'^ISODate\("[0-9\-T\:\.]*Z"\)$', fieldValue):
            #                 fieldValue = fieldValue.replace('ISODate("', '').replace('")', '')
            #                 fieldValue = datetime.datetime.strptime(fieldValue, '%Y-%m-%dT%H:%M:%S.%fZ');
            #         elif isinstance(fieldValue, dict):
            #             print(fieldValue)



            #         document[fieldName] = fieldValue
            #     newDocumentList.append(document)
            # print(newDocumentList)
            db.get_collection(collectionName).insert_many(documents)


@pytest.fixture
def client(app: Flask):
    """A test client for the app."""
    return app.test_client()