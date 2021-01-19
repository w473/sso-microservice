import uuid
from flask import Blueprint, abort, request, current_app
from passlib.hash import sha256_crypt
from flaskr.domain.db import getDb
from flaskr.services.JwtService import encodeJwt, getSysJwt
from flaskr.services.AuthService import is_logged, parseToken
from flaskr.services.AppsAuthorizationService import isAppCredentialValid
from flaskr.domain.repositories.RefreshTokenRepository import RefreshTokenRepository
from flaskr.domain.documents.RefreshToken import RefreshToken
from flaskr.services import UserService, RequestService

controller = Blueprint('auth', __name__, url_prefix='/auth')


@controller.route("/sysLogin", methods=['POST'])
@RequestService.validate(kind='syslogin')
def sysLogin():
    """Endpoint for getting JWT token by other services
    ---
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    properties:
                        app:
                            type: string
                        key:
                            type: string
    responses:
        200:
            description: JWT Token
            content:
                text/plain:
                    schema:
                        type: string
        400:
            description: Invalid Request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Message'
        403:
            description: Not allowed
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Message'
    """
    content = request.get_json(silent=True)
    if content == None:
        return {'message': 'Invalid request - no json'}, 400

    key = content.get('key')
    app = content.get('app')

    if key == None or app == None:
        return {'message': 'Invalid request'}, 400

    if isAppCredentialValid(app, key):
        return getSysJwt(app), 200

    return {"message": "Not allowed"}, 403


@controller.route("/login", methods=['POST'])
@RequestService.validate(kind='login')
def login():
    """Endpoint for getting JWT token by users
    ---
    requestBody:
        required: true
        content:
            application/json:
                schema:
                    properties:
                        app:
                            type: string
                        key:
                            type: string
    definitions:
      Message:
        type: object
        properties:
          message:
            type: string
    responses:
        200:
            description: JWT Token
            content:
                text/plain:
                    schema:
                        type: string
        400:
            description: Invalid Request
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Message'
        403:
            description: Not allowed
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Message'
    """
    content = request.get_json(silent=True)
    if content == None:
        return {'message': 'Invalid request - no json'}, 400

    email = content.get('email')
    password = content.get('password')

    if email == None or password == None:
        return {'message': 'Invalid request'}, 400

    user = UserService.findUser(email, {"password": password})

    if user == None:
        return {'message': 'Login failed'}, 403

    current_app.logger.info(user)

    if user.isActive == False:
        return {'message': 'Please activate your account'}, 403

    refreshToken = RefreshToken(user.id, str(uuid.uuid4()))

    (RefreshTokenRepository(getDb())).save(refreshToken)

    payload = user.toDict()
    payload['refreshToken'] = refreshToken.token

    return encodeJwt(payload), 200


@controller.route("/logout", methods=['POST'])
@is_logged()
def logout():
    # remove all refresh tokens?
    return {}


@controller.route("/tokenRefresh", methods=['GET'])
def refreshToken():
    """Endpoint for getting refreshed JWT token by users
    ---
    responses:
        200:
            description: JWT Token
            content:
                text/plain:
                    schema:
                        type: string
        403:
            description: Not allowed
            content:
                application/json:
                    schema:
                        $ref: '#/definitions/Message'
    """
    try:
        token = parseToken(True)
        refreshToken = token.get('refreshToken')
        email = token.get('email')
        if refreshToken:
            user = UserService.findUser(email, {})
            tokenRepo = RefreshTokenRepository(getDb())
            if user and tokenRepo.exist(refreshToken, user.id):
                tokenRepo.delete(refreshToken)
                refreshToken = RefreshToken(user.id, str(uuid.uuid4()))
                tokenRepo.save(refreshToken)
                payload = user.toDict()
                payload['refreshToken'] = refreshToken.token
                return encodeJwt(payload), 200
    except Exception as e:
        current_app.logger.info(e)

    return {"message": "Not allowed"}, 403
