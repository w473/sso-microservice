import pytest
from flask.testing import FlaskClient

#auth
def testLogin(client):
    #all wrong
    response = client.post("/auth/login")
    assert response.data == b"{\"message\":\"Invalid request\"}\n"
    assert response.status_code == 400

    #no username and pass
    response = client.post("/auth/login", json={})
    assert response.data == b"{\"message\":\"Invalid request\"}\n"
    assert response.status_code == 400

    #no password
    response = client.post("/auth/login", json={"username": 'username'})
    assert response.data == b"{\"message\":\"Invalid request\"}\n"
    assert response.status_code == 400

    #wrong user/pass
    response = client.post("/auth/login", json={"username": 'username', "password": 'password'})
    assert response.data == b"{\"message\":\"Login failed\"}\n"
    assert response.status_code == 403

    #not active
    response = client.post("/auth/login", json={"username": 'notactive', "password": 'pass'})
    assert response.data == b"{\"message\":\"Please activate your account\"}\n"
    assert response.status_code == 403

    #ok
    response = client.post("/auth/login", json={"username": 'testuser', "password": 'pass'})
    assert response.status_code == 200

def testTokenRefresh(client, authHeader):
    response = client.get('/auth/tokenRefresh')
    assert response.status_code == 403
    assert response.data == b'{"message":"Not allowed"}\n'

    response = client.get('/auth/tokenRefresh', headers=authHeader)
    assert response.status_code == 200
    assert len(response.get_data( as_text = True )) > 500