import pytest
from flask.testing import FlaskClient

# key


def testKeyGenerateUser(client, authHeader):
    response = client.put('/key/generate')
    assert response.status_code == 403
    assert response.data == b'{\n  "message": "Authorization header not found"\n}\n'

    response = client.put('/key/generate', headers=authHeader)
    assert response.status_code == 403
    assert response.data == b'{\n  "message": "Not allowed"\n}\n'


def testKeyGenerateAdmin(client, authHeaderAdmin):
    response = client.put('/key/generate', headers=authHeaderAdmin)
    print(response.data)
    assert response.status_code == 204
    assert response.data == b''


def testKeyGetUser(client, authHeader):
    response = client.get('/key/5fac4e4d95d76284e10e35b2')
    assert response.status_code == 403
    assert response.data == b'{\n  "message": "Authorization header not found"\n}\n'

    response = client.get('/key/5fac4e4d95d76284e10e35b2', headers=authHeader)
    assert response.status_code == 403
    assert response.data == b'{\n  "message": "Not allowed"\n}\n'


def testKeyGetAdmin(client, authHeaderAdmin):
    response = client.get('/key/444',
                          headers=authHeaderAdmin)
    assert response.status_code == 404
    assert response.data == b'{\n  "message": "Key has not been found"\n}\n'

    response = client.get('/key/wrongkey', headers=authHeaderAdmin)
    assert response.status_code == 404
    assert response.data == b'{\n  "message": "Key has not been found"\n}\n'

    response = client.get('/key/1',
                          headers=authHeaderAdmin)
    assert response.status_code == 200
    assert b'BEGIN PUBLIC KEY' in response.data


def testKeyListAllUser(client: FlaskClient, authHeader: dict):
    response = client.get('/key')
    assert response.status_code == 200
    assert len(response.get_json().get('keys')) == 2

    response = client.get('/key', headers=authHeader)
    assert response.status_code == 200
    assert len(response.get_json().get('keys')) == 2


def testKeyListAllAdmin(client: FlaskClient, authHeaderAdmin: dict):
    response = client.get('/key', headers=authHeaderAdmin)
    assert response.status_code == 200
    assert len(response.get_json().get('keys')) == 2


def testKeyDeleteUser(client, authHeader):
    response = client.delete('/key/1')
    assert response.status_code == 403
    assert response.data == b'{\n  "message": "Authorization header not found"\n}\n'

    response = client.delete('/key/1', headers=authHeader)
    assert response.status_code == 403
    assert response.data == b'{\n  "message": "Not allowed"\n}\n'


def testKeyDeleteAdmin(client, authHeaderAdmin):
    response = client.delete('/key/asdasd', headers=authHeaderAdmin)
    assert response.status_code == 400
    assert response.data == b'{\n  "message": "Key id is invalid"\n}\n'

    response = client.delete(
        '/key/444', headers=authHeaderAdmin)
    assert response.status_code == 404
    assert response.data == b'{\n  "message": "Key has not been found"\n}\n'

    response = client.delete(
        '/key/1', headers=authHeaderAdmin)
    assert response.status_code == 204
    assert response.data == b''
