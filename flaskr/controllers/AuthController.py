from flask import Blueprint, abort, request, current_app
from passlib.hash import sha256_crypt
from flaskr.domain.mongo import getDb
from flaskr.services.JwtService import encodeJwt
from flaskr.services.AuthService import is_logged, parseToken
from flaskr.domain.repositories.UserRepository import UserRepository 
from flaskr.domain.repositories.RefreshTokenRepository import RefreshTokenRepository 
from flaskr.domain.documents.RefreshToken import RefreshToken
import uuid

controller = Blueprint('auth', __name__, url_prefix='/auth')

@controller.route("/login", methods=['POST'])
def login():
    content = request.get_json(silent=True)
    if content == None:
        return {'message': 'Invalid request'}, 400

    username = content.get('username')
    password = content.get('password')

    if username == None or password == None:
        return {'message': 'Invalid request'}, 400

    repo = UserRepository(getDb())
    user = repo.findByUsername(username)
    
    if user == None or sha256_crypt.verify(password, user.password) == False:
        return {'message': 'Login failed'}, 403

    if user.isActive == False:
        return {'message': 'Please activate your account'}, 403

    refreshToken = RefreshToken(user.id, str(uuid.uuid4()))
    (RefreshTokenRepository(getDb())).save(refreshToken)

    payload = user.toDictResponse()
    payload['refreshToken'] = refreshToken.token
    

# moze response jakos inaczej? tak zeby latwo refresh token?

    return encodeJwt(payload), 200

@controller.route("/logout", methods=['POST'])
@is_logged()
def logout():
    # remove all refresh tokens?
    return {}

@controller.route("/tokenRefresh", methods=['GET'])
def refreshToken():
    try:
        token = parseToken(False)
        refreshToken = token.get('refreshToken')
        username = token.get('username')
        if refreshToken:
            userRepo = UserRepository(getDb())
            user = userRepo.findByUsername(username)
            tokenRepo = RefreshTokenRepository(getDb())
            if user and tokenRepo.exist(refreshToken, user.id): 
                tokenRepo.delete(refreshToken)
                refreshToken = RefreshToken(user.id, str(uuid.uuid4()))
                tokenRepo.save(refreshToken)

                payload = user.toDictResponse()
                payload['refreshToken'] = refreshToken.token
                return encodeJwt(payload), 200
    except Exception as e:
        current_app.logger.info(e)

    return {"message": "Not allowed"}, 403

