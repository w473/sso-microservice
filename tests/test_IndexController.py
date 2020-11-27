import pytest
from flask.testing import FlaskClient

#index
def testIndex(client):
    response = client.get("/")
    assert b"Welcome to Trakayo SSO" in response.data