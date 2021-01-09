from flask import g, current_app, Request, request, jsonify
from functools import wraps
from flaskr.services.JwtService import decodeJwt, JWTExpiredException
from flaskr.domain.db import getDb
from flaskr.domain.documents.User import User
from flaskr.services import UserService
from jwt.exceptions import ExpiredSignatureError
import logging
import sys
import traceback

logger = logging.getLogger(__name__)


def parseToken(allowExpired: bool = False) -> dict:
    if 'Authorization' in request.headers:
        tokenString = request.headers['Authorization']
    else:
        raise AuthorizationException('Authorization header not found')
    if not tokenString:
        raise AuthorizationException('Valid token is missing')

    try:
        return decodeJwt(tokenString.replace('Bearer ', '', 1))
    except JWTExpiredException as e:
        if allowExpired:
            return e.payload
        else:
            raise e
    except ExpiredSignatureError as e:
        raise AuthorizationException('Token expired')
    except Exception as e:
        logger.info(e)
        raise AuthorizationException('Token is invalid')


def authorize() -> User:
    try:
        token = parseToken()
        email = token.get('email')
        user = UserService.findUser(email, {})
        if user:
            logger.info('User found: '+email)
        else:
            logger.info('User not found: ' + email)
            raise AuthorizationException('Token is invalid - user not found')
        print(user.id)
        return user
    except AuthorizationException as e:
        raise e
    except ExpiredSignatureError as e:
        raise AuthorizationException('Token expired')
    except Exception as e:
        logger.error(e)
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
                print(e)
                return jsonify({'message': e.getMessage()}), 403
        return wrapper
    return decorator


class AuthorizationException(Exception):
    def __init__(self, message: str):
        self.message = message

    def getMessage(self) -> str:
        return self.message
