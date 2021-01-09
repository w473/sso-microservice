import pytest
import json
import sys
import re
import datetime
import uuid
import responses
from flask import Flask
from flaskr import create_app
from flaskr.domain import db
from flask.testing import FlaskClient
from helper import setUserAdmin, setUserNormal


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    testConfig = {
        'SECRET_KEY': 'potato',
        'DB_HOSTNAME': "localhost",
        'DB_USERNAME': "root",
        'DB_PASSWORD': "password",
        'DB_NAME': "test_sso",
        'USERS_SERVICE_URL': "potatoURL",
        'MAILING_SERVER': ""
    }

    app = create_app(testConfig)

    # create the database and load test data
    with app.app_context():
        initDB()

    yield app


def initDB():
    connection = db.getDb()

    db.destroyDb()
    db.initDb()
    with open('tests/db.json') as json_file:
        data = json.load(json_file)

        for dbName, rows in data.items():
            for row in rows:
                values = list(row.values())
                sql = "INSERT INTO `{}` (".format(dbName)
                sql += ",".join(row.keys())
                sql += ") VALUES (" + ', '.join((['%s'] * len(values)))+");"

                newVals = list()
                for val in values:
                    if type(val) is dict:
                        newVals.append(uuid.UUID(val.get('value')).bytes)
                    else:
                        newVals.append(val)
                with connection.cursor() as cursor:
                    cursor.execute(sql, newVals)

                connection.commit()


@pytest.fixture
def client(app: Flask):
    return app.test_client(use_cookies=False)


@pytest.fixture
def authHeader(app: Flask, client) -> dict:
    setUserNormal(app)
    response = client.post(
        "/auth/login", json={"email": 'testuser', "password": 'pass'}
    )
    token = response.get_data(as_text=True)

    return {"Authorization": "Bearer " + token}


@pytest.fixture
def authHeaderAdmin(app: Flask, client) -> dict:
    setUserAdmin(app)
    response = client.post(
        "/auth/login", json={"email": 'testuseradmin', "password": 'pass'}
    )
    token = response.get_data(as_text=True)

    return {"Authorization": "Bearer " + token}
