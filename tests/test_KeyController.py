import pytest
from flask.testing import FlaskClient

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


def testKeyDelete(client, authHeader, authHeaderAdmin):
    response = client.delete('/key/5fac4e4d95d76284e10e35b2')
    assert response.status_code == 403
    assert response.data == b'{"message":"Authorization header not found"}\n'

    response = client.delete('/key/5fac4e4d95d76284e10e35b2', headers=authHeader)
    assert response.status_code == 403
    assert response.data == b'{"message":"Not allowed"}\n'

    response = client.delete('/key/asdasd', headers=authHeaderAdmin)
    assert response.status_code == 400
    assert response.data == b'{"message":"Key id is invalid"}\n'

    response = client.delete('/key/5fc00e7a4e303905dfca7975', headers=authHeaderAdmin)
    assert response.status_code == 404
    assert response.data == b'{"message":"Key has not been found"}\n'

    response = client.delete('/key/5fc00a35503b577f395db5f7', headers=authHeaderAdmin)
    assert response.status_code == 204
    assert response.data == b''

    