import pytest
from flask.testing import FlaskClient
from helper import setUserNotActive, setUserNormal, setUserNotFound, jsonCompareDict
import base64
import json
# auth


def testLoginWrong(client):
    # all wrong
    response = client.post("/auth/login")
    assert response.data == b'{\n  "message": "Invalid request - no json"\n}\n'
    assert response.status_code == 400

    # no username and pass
    response = client.post("/auth/login", json={})
    assert response.data == b'{\n  "message": "Invalid request"\n}\n'
    assert response.status_code == 400

    # no password
    response = client.post("/auth/login", json={"email": 'email'})
    assert response.data == b'{\n  "message": "Invalid request"\n}\n'
    assert response.status_code == 400


def testLoginNotFound(app, client):
    setUserNotFound(app)
    response = client.post(
        "/auth/login", json={"email": 'email', "password": 'password'})
    print(response.data)
    assert response.data == b'{\n  "message": "Login failed"\n}\n'
    assert response.status_code == 403


def testLoginNotActive(app, client):
    setUserNotActive(app)
    response = client.post(
        "/auth/login", json={"email": 'notactive', "password": 'pass'})
    assert response.data == b'{\n  "message": "Please activate your account"\n}\n'
    assert response.status_code == 403


def testLoginOk(app, client):
    setUserNormal(app)
    response = client.post(
        "/auth/login", json={"email": 'testuser', "password": 'pass'})
    assert response.status_code == 200


def testTokenRefresh(client, authHeader):
    response = client.get('/auth/tokenRefresh')
    assert response.status_code == 403
    assert response.data == b'{\n  "message": "Not allowed"\n}\n'

    response = client.get('/auth/tokenRefresh', headers=authHeader)
    assert response.status_code == 200
    assert len(response.get_data(as_text=True)) > 500


def testSysLogin(client):
    response = client.post('/auth/sysLogin')
    assert response.status_code == 400
    jsonCompareDict(
        response.data,
        {
            'data': {'': 'None is not of type \'object\''},
            'message': "Validation failed"
        }
    )
    response = client.post(
        "/auth/sysLogin", json={"email": 'testuser', "password": 'pass'})
    assert response.status_code == 400

    response = client.post(
        "/auth/sysLogin", json={"app": 'mailers', "key": 'mailer_passwords'})
    assert response.status_code == 403
    jsonCompareDict(response.data, {'message': "Not allowed"})

    response = client.post(
        "/auth/sysLogin", json={"app": 'mailer', "key": 'mailer_password'})
    assert response.status_code == 200

    dictFromJson = json.loads(
        base64.b64decode(
            response.data.decode().split('.')[1]
        ).decode()
    )
    assert dictFromJson.get('email') == 'system'
    assert dictFromJson.get('username') == 'mailer'
    assert dictFromJson.get('roles') == ['SYS', 'ADMIN']
