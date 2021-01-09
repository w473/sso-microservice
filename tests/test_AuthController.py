import pytest
from flask.testing import FlaskClient
from helper import setUserNotActive, setUserNormal, setUserNotFound
# auth


def testLoginWrong(client):
    # all wrong
    response = client.post("/auth/login")
    assert response.data == b'{"message":"Invalid request - no json"}\n'
    assert response.status_code == 400

    # no username and pass
    response = client.post("/auth/login", json={})
    assert response.data == b"{\"message\":\"Invalid request\"}\n"
    assert response.status_code == 400

    # no password
    response = client.post("/auth/login", json={"email": 'email'})
    assert response.data == b"{\"message\":\"Invalid request\"}\n"
    assert response.status_code == 400


def testLoginNotFound(app, client):
    setUserNotFound(app)
    response = client.post(
        "/auth/login", json={"email": 'email', "password": 'password'})
    print(response.data)
    assert response.data == b"{\"message\":\"Login failed\"}\n"
    assert response.status_code == 403


def testLoginNotActive(app, client):
    setUserNotActive(app)
    response = client.post(
        "/auth/login", json={"email": 'notactive', "password": 'pass'})
    assert response.data == b"{\"message\":\"Please activate your account\"}\n"
    assert response.status_code == 403


def testLoginOk(app, client):
    setUserNormal(app)
    response = client.post(
        "/auth/login", json={"email": 'testuser', "password": 'pass'})
    assert response.status_code == 200


def testTokenRefresh(client, authHeader):
    response = client.get('/auth/tokenRefresh')
    assert response.status_code == 403
    assert response.data == b'{"message":"Not allowed"}\n'

    response = client.get('/auth/tokenRefresh', headers=authHeader)
    print(response.get_data(as_text=True))
    assert response.status_code == 200
    assert len(response.get_data(as_text=True)) > 500
