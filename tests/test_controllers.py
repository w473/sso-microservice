import pytest

def testIndex(client):
    response = client.get("/")
    assert b"Welcome to Trakayo SSO" in response.data

def testLogin(client):
    #all wrong
    response = client.post("/auth/login/username/password")
    assert response.data == b"{\"message\":\"Login failed\"}\n"
    assert response.status_code == 403

    #not active
    response = client.post("/auth/login/notactive/pass")
    assert response.data == b"{\"message\":\"Please activate your account\"}\n"
    assert response.status_code == 403

    #ok
    response = client.post("/auth/login/testuser/pass")
    assert response.status_code == 200