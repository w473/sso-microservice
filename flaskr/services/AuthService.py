from flask import g, current_app, Request, request, jsonify
from functools import wraps
from flaskr.services.JwtService import decodeJwt
from flaskr.domain.mongo import getDb
from flaskr.domain.repositories.UserRepository import UserRepository
from flaskr.domain.documents.User import User
from jwt import ExpiredSignature
import logging

logger = logging.getLogger( __name__ )

def parseToken(notAllowExpired: bool = True) -> dict:
    if 'Authorization' in request.headers:
        tokenString = request.headers['Authorization']
    else:
        raise AuthorizationException('Authorization header not found')
    if not tokenString:
        raise AuthorizationException('Valid token is missing')

    try:
        return decodeJwt(tokenString.replace('Bearer ', '', 1), notAllowExpired)
    except ExpiredSignature as e:
        raise AuthorizationException('Token expired')
    except Exception as e:
        logger.info(tokenString)
        logger.info(e)
        raise AuthorizationException('Token is invalid')

def authorize() -> User:
    try:
        token = parseToken()
        repo = UserRepository(getDb())
        username = token.get('username')
        user = repo.findByUsername(username)
        if user:
            logger.info('User found: '+username)
        else:
            logger.info('User not found: '+ username)
            raise AuthorizationException('Token is invalid - user not found')
        return user
    except AuthorizationException as e:
        raise e
    except ExpiredSignature as e:
        raise AuthorizationException('Token expired')
    except Exception as e:
        logger.info(e)
        raise AuthorizationException('Token is invalid')

def is_logged(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                user = authorize()
                if role != None:
                    if user.isActive == False:
                        return {'message': 'Not allowed'}, 403

                    if user.hasRole(role):
                        g.user = user
                        return func(*args, **kwargs)
                    else:
                        return {'message': 'Not allowed'}, 403
                g.user = user
                return func(*args, **kwargs)
            except AuthorizationException as e:
                return jsonify({'message': e.getMessage()}), 403
        return wrapper
    return decorator

class AuthorizationException(Exception):
    def __init__(self, message: str):
        self.message = message

    def getMessage(self) -> str:
        return self.message