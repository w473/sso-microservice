from flask import Blueprint, abort, request, current_app
from passlib.hash import sha256_crypt
from ..domain.mongo import getDb
from ..services.JwtService import encodeJwt
from flaskr.services.AuthService import is_logged, parseToken
from ..domain.repositories.UserRepository import UserRepository 
from ..domain.repositories.RefreshTokenRepository import RefreshTokenRepository 
from ..domain.documents.RefreshToken import RefreshToken
import uuid

app = Blueprint('auth', __name__, url_prefix='/auth')

@app.route("/login/<username>/<password>", methods=['POST'])
def login(username, password):
    repo = UserRepository(getDb())

    user = repo.findByUsername(username)
    
    if user == None or sha256_crypt.verify(password, user.password) == False:
        return {'status' : 'fail', 'message': 'user nie ma albo haslo zle'}, 403

    refreshToken = RefreshToken(user.id, str(uuid.uuid4()))
    (RefreshTokenRepository(getDb())).save(refreshToken)

    payload = user.toDictResponse()
    payload['refreshToken'] = refreshToken.token
    

# moze response jakos inaczej? tak zeby latwo refresh token?

    return encodeJwt(payload), 200

@app.route("/logout", methods=['POST'])
@is_logged
def logout():
    # i teraz ogarnoc login przez Jwt
    # i automatyczne wydawanie nowego tokenu jak nie wazny
    return {}

@app.route("/tokenRefresh", methods=['GET'])
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
                current_app.logger.info('istniie refhres')
                tokenRepo.delete(refreshToken)
                refreshToken = RefreshToken(user.id, str(uuid.uuid4()))
                tokenRepo.save(refreshToken)

                payload = user.toDictResponse()
                payload['refreshToken'] = refreshToken.token
                return encodeJwt(payload), 200
    except Exception as e:
        current_app.logger.info(e)

    return {"message": "Not Allowed"}, 403

