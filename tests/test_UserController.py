import pytest
from flask.testing import FlaskClient

#user
def testUserCreate(client: FlaskClient):
    response = client.post('/user')
    assert response.status_code == 400
    assert response.data == b'{"data":{"":"None is not of type \'object\'"}}\n'
    
    json = {
        'username' : 'tesasdasd',
    }

    response = client.post('/user', json=json)
    assert response.status_code == 400
    assert response.data == b'{"data":{"":"\'password\' is a required property"}}\n'

    json = {
        'username' : 'tesasdasd',
        'password' : 'tesasdasd',
    }

    response = client.post('/user', json=json)
    assert response.status_code == 400
    assert response.data == b'{"data":{"":"\'locale\' is a required property"}}\n'

    json = {
        'username' : 'tesasdasd',
        'password' : 'tesasdasd',
        'locale' : 'pl_PL',
    }

    response = client.post('/user', json=json)
    assert response.status_code == 400
    assert response.data == b'{"data":{"":"\'email\' is a required property"}}\n'

    json = {
        'username' : 'tesasdasd',
        'locale' : 'pl_PL',
        'email' : 'test1@asd.pl',
        'password' : 'tesasdasd',
    }

    response = client.post('/user', json=json)
    assert response.status_code == 400
    assert response.data == b'{"data":{"":"\'publicName\' is a required property"}}\n'

    json = {
        'username' : 'tes',
        'publicName' : 'te1',
        'email' : 'test1',
        'locale' : 'test1',
        'password' : 'tes',
    }

    response = client.post('/user', json=json)
    assert response.status_code == 400
    assert response.json == {
        'data': {
            'email': "'test1' does not match '[a-z0-9\\\\._%+!$&*=^|~#%{}/\\\\-]+@([a-z0-9\\\\-]+\\\\.){1,}([a-z]{2,22})'",
            'locale': "'test1' does not match '^[a-z][a-z]_[A-Z][A-Z]$'",
            'password': "'tes' is too short",
            'publicName': "'te1' is too short", 
            'username': "'tes' is too short"
        }
    }
    
    json = {
        'username' : 'test',
        'publicName' : 'test',
        'email' : 'test1@tsasd.pl',
        'locale' : 'en_GB',
        'password' : 'tesddd',
    }

    response = client.post('/user', json=json)
    assert response.status_code == 204
    assert response.data == b''

    json = {
        'username' : 'testasda',
        'publicName' : 'test',
        'email' : 'notreal@emailaa.tv',
        'locale' : 'en_GB',
        'password' : 'tesddd',
    }

    response = client.post('/user', json=json)
    assert response.status_code == 400
    assert response.data == b'{"message":"You cannot use this email address"}\n'

    json = {
        'username' : 'notactive',
        'publicName' : 'test',
        'email' : 'notreal@emailsaa.tv',
        'locale' : 'en_GB',
        'password' : 'tesddd',
    }

    response = client.post('/user', json=json)
    assert response.status_code == 400
    assert response.data == b'{"message":"Please choose different username"}\n'

#UserUpdate
def testUserUpdate(client: FlaskClient, authHeader: dict):
    userUpdate(client, authHeader)

    json = {
        'publicName' : 'te1asdfasd'
    }

    response = client.patch('/user/porato', json=json, headers=authHeader)
    print(response.data)
    assert response.status_code == 403
    assert response.data == b'{"message":"Not allowed"}\n'

def testUserUpdateAdmin(client: FlaskClient, authHeaderAdmin: dict):
    userUpdate(client, authHeaderAdmin, '/testuser')

def userUpdate(client: FlaskClient, authHeader: dict, username=''):
    response = client.patch('/user'+username)
    assert response.status_code == 403
    assert response.data == b'{"message":"Authorization header not found"}\n'

    response = client.patch('/user'+username, headers=authHeader)
    assert response.status_code == 400
    assert response.data == b'{"data":{"":"None is not of type \'object\'"}}\n'
    
    json = {
        'username' : 'tes',
        'publicName' : 'te1',
        'email' : 'test1',
        'locale' : 'test1',
        'password' : 'tes',
    }

    response = client.patch('/user'+username, json=json, headers=authHeader)
    assert response.status_code == 400
    assert response.json == {
        'data': {
            'email': "'test1' does not match '[a-z0-9\\\\._%+!$&*=^|~#%{}/\\\\-]+@([a-z0-9\\\\-]+\\\\.){1,}([a-z]{2,22})'",
            'locale': "'test1' does not match '^[a-z][a-z]_[A-Z][A-Z]$'",
            'password': "'tes' is too short",
            'publicName': "'te1' is too short", 
            'username': "'tes' is too short"
        }
    }
    
    json = {
        'publicName' : 'test',
        'locale' : 'en_GB',
        'password' : 'tesddd',
    }

    response = client.patch('/user'+username, json=json, headers=authHeader)
    assert response.status_code == 204
    assert response.data == b''

    json = {
        'publicName' : 'test',
        'email' : 'notreal@emailaa.tv',
        'locale' : 'en_GB',
        'password' : 'tesddd',
    }

    response = client.patch('/user'+username, json=json, headers=authHeader)
    assert response.status_code == 400
    assert response.data == b'{"message":"You cannot use this email address"}\n'

    json = {
        'username' : 'notactive',
        'publicName' : 'test',
        'email' : 'notreal@emailsaa.tv',
        'locale' : 'en_GB',
        'password' : 'tesddd',
    }

    response = client.patch('/user'+username, json=json, headers=authHeader)
    assert response.status_code == 400
    assert response.data == b'{"message":"Please choose different username"}\n'
    
    json = {
        'publicName' : 'test',
        'email' : 'test1@tsasd.pl',
        'locale' : 'en_GB',
        'password' : 'tesddd',
    }

    response = client.patch('/user'+username, json=json, headers=authHeader)
    assert response.status_code == 200
    assert response.data == b'{"message":"Please activate your email"}\n'

def testActivate(client: FlaskClient):
    response = client.patch('/user/sssss/activate/someactivationcode')
    assert response.status_code == 400
    assert response.data == b'{"message":"Wrong username"}\n'

    response = client.patch('/user/notactive/activate/someasssctivationcode')
    assert response.status_code == 400
    assert response.data == b'{"message":"Wrong activation code"}\n'

    response = client.patch('/user/notactive/activate/someactivationcode')
    assert response.status_code == 204
    assert response.data == b''

def testGetUser(client: FlaskClient, authHeader: dict, authHeaderAdmin: dict):
    response = client.get('/user')
    assert response.status_code == 403
    assert response.data == b'{"message":"Authorization header not found"}\n'

    response = client.get('/user', headers=authHeader)
    assert response.status_code == 200
    assert response.json == {
        'data': {
            'create': '11/24/2020, 20:11:46', 
            'email': 'notreal@emailaa2.tv', 
            'isActive': True, 
            'locale': 'pl_PL', 
            'publicName': 'test user', 
            'roles': ['USER'], 
            'username': 'testuser'
            }
        }

    response = client.get('/user/notactive', headers=authHeader)
    assert response.status_code == 403
    assert response.data == b'{"message":"Not allowed"}\n'

    response = client.get('/user/notactive', headers=authHeaderAdmin)
    assert response.status_code == 200
    assert response.json == {
        'data': {
            'create': '11/24/2020, 20:11:46', 
            'email': 'notreal@emailaa.tv', 
            'isActive': False, 
            'locale': 'pl_PL', 
            'publicName': 'not active user', 
            'roles': ['USER'], 
            'username': 'notactive'
            }
        }

    response = client.get('/user/asdasd', headers=authHeaderAdmin)
    assert response.status_code == 400
    assert response.data == b'{"message":"User does not exists"}\n'

def testDeleteUser(client: FlaskClient, authHeader: dict, authHeaderAdmin: dict):
    response = client.delete('/user')
    assert response.status_code == 403
    assert response.data == b'{"message":"Authorization header not found"}\n'

    response = client.delete('/user/something', headers=authHeader)
    assert response.status_code == 403
    assert response.data == b'{"message":"Not allowed"}\n'

    response = client.delete('/user/something', headers=authHeaderAdmin)
    assert response.status_code == 400
    assert response.data == b'{"message":"User not found"}\n'

    response = client.delete('/user/notactive', headers=authHeaderAdmin)
    assert response.status_code == 204
    assert response.data == b''

    response = client.delete('/user', headers=authHeader)
    assert response.status_code == 204
    assert response.data == b''