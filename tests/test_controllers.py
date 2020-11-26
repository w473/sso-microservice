import pytest
from flask.testing import FlaskClient

#index
def testIndex(client):
    response = client.get("/")
    assert b"Welcome to Trakayo SSO" in response.data

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

#key
def testKeyGenerate(client, authHeader, authHeaderAdmin):
    response = client.put('/key/generate')
    assert response.status_code == 403
    assert response.data == b'{"message":"Authorization header not found"}\n'
    
    response = client.put('/key/generate', headers=authHeader)
    assert response.status_code == 403
    assert response.data == b'{"message":"Not allowed"}\n'
    
    response = client.put('/key/generate', headers=authHeaderAdmin)
    print(response.data)
    assert response.status_code == 204
    assert response.data == b''  

def testKeyGet(client, authHeader, authHeaderAdmin):
    response = client.get('/key/5fac4e4d95d76284e10e35b2')
    assert response.status_code == 403
    assert response.data == b'{"message":"Authorization header not found"}\n'
    
    response = client.get('/key/5fac4e4d95d76284e10e35b2', headers=authHeader)
    assert response.status_code == 403
    assert response.data == b'{"message":"Not allowed"}\n'
    
    response = client.get('/key/5fc00e7a4e303905dfca7975', headers=authHeaderAdmin)
    assert response.status_code == 404
    assert response.data == b'{"message":"Key has not been found"}\n'

    response = client.get('/key/wrongkey', headers=authHeaderAdmin)
    assert response.status_code == 400
    assert response.data == b'{"message":"Key id is invalid"}\n'

    response = client.get('/key/5fc00a3efe85299614e1217b', headers=authHeaderAdmin)
    assert response.status_code == 200
    assert b'BEGIN PUBLIC KEY' in response.data

def testKeyListAll(client: FlaskClient, authHeader: dict, authHeaderAdmin: dict):
    response = client.get('/key')
    assert response.status_code == 403
    assert response.data == b'{"message":"Authorization header not found"}\n'
    
    response = client.get('/key', headers=authHeader)
    assert response.status_code == 403
    assert response.data == b'{"message":"Not allowed"}\n'
    
    response = client.get('/key', headers=authHeaderAdmin)
    assert response.status_code == 200
    assert len(response.get_json()) == 2

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

# def testUserUpdate(client: FlaskClient):
#     response = client.patch('/user')
#     assert response.status_code == 400
#     assert response.data == b'{"data":{"":"None is not of type \'object\'"}}\n'
    
#     json = {
#         'username' : 'tes',
#         'publicName' : 'te1',
#         'email' : 'test1',
#         'locale' : 'test1',
#         'password' : 'tes',
#     }

#     response = client.patch('/user', json=json)
#     assert response.status_code == 400
#     assert response.json == {
#         'data': {
#             'email': "'test1' does not match '[a-z0-9\\\\._%+!$&*=^|~#%{}/\\\\-]+@([a-z0-9\\\\-]+\\\\.){1,}([a-z]{2,22})'",
#             'locale': "'test1' does not match '^[a-z][a-z]_[A-Z][A-Z]$'",
#             'password': "'tes' is too short",
#             'publicName': "'te1' is too short", 
#             'username': "'tes' is too short"
#         }
#     }
    
#     json = {
#         'username' : 'test',
#         'publicName' : 'test',
#         'email' : 'test1@tsasd.pl',
#         'locale' : 'en_GB',
#         'password' : 'tesddd',
#     }

#     response = client.patch('/user', json=json)
#     assert response.status_code == 204
#     assert response.data == b''

#     json = {
#         'username' : 'testasda',
#         'publicName' : 'test',
#         'email' : 'notreal@emailaa.tv',
#         'locale' : 'en_GB',
#         'password' : 'tesddd',
#     }

#     response = client.patch('/user', json=json)
#     assert response.status_code == 400
#     assert response.data == b'{"message":"You cannot use this email address"}\n'

#     json = {
#         'username' : 'notactive',
#         'publicName' : 'test',
#         'email' : 'notreal@emailsaa.tv',
#         'locale' : 'en_GB',
#         'password' : 'tesddd',
#     }

#     response = client.patch('/user', json=json)
#     assert response.status_code == 400
#     assert response.data == b'{"message":"Please choose different username"}\n'