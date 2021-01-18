from flaskr.domain.documents.User import User
from flaskr.services.JwtService import encodeJwt, getSysJwt
from flaskr.services.RequestService import getRequest
from flask import current_app


def findUser(email: str, params: dict) -> User:

    url = '/findByEmail'

    payload = {'email': email}
    if 'password' in params:
        payload['password'] = params['password']
        url = '/findByEmailPassword'
    elif len(params) != 0:
        raise Exception('Not implemented')

    url = current_app.config['USERS_SERVICE_URL'] + url

    headers = {'Authorization': 'Bearer ' + getSysJwt('sso')}

    r = getRequest().post(url, payload, headers)

    response = r.json()
    if r.status_code in [400, 403, 404]:
        return None
    if r.status_code != 200:
        raise Exception(response['message'])

    return User(response.get('data'))
