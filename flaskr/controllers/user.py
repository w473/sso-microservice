from flask import Blueprint, request, current_app
from pymongo.errors import DuplicateKeyError
from datetime import datetime
from passlib.hash import sha256_crypt
from ..domain.documents.User import User
from ..domain.repositories.UserRepository import UserRepository 
from ..domain.mongo import getDb
from ..formatters.UserFormatter import forApiAsDict
from flaskr.services.AuthService import is_logged
from flaskr.services.RequestService import validate

import logging
logger = logging.getLogger( __name__ )

app = Blueprint('user', __name__, url_prefix='/user')

@app.route("", methods=['POST'])
@validate(kind='user')
def create():
    content = request.get_json(silent=True)
    logger.error(content)
    if content == None:
        return {'status' : 'fail', 'message': 'dupa'}, 400

    user = User(content)
    try:
        user.setCreate(datetime.utcnow())
        user.setEnabled(False)
        password = sha256_crypt.encrypt(content.get('password'))
        user.setPassword(password)
        repo = UserRepository(getDb())
        repo.add(user)
    except DuplicateKeyError:
        return {'status' : 'fail', 'message': 'User already exists! - this error should not be here'}, 400

    return '', 204

@app.route("", methods=['PATCH'], defaults={'username': None})
@app.route("/<username>", methods=['PATCH'])
@validate(kind='user')
@is_logged
def update(user: User, username: str):
    repo = UserRepository(getDb())
    if username == None:
        pass
    elif user.hasRole('admin') and username != None:
        user = repo.findByUsername(username)
        if user == None:
            return {'status' : 'fail', 'message': 'User not found'}, 400
    else:
        return {'status' : 'fail', 'message': 'Forbidden'}, 403

    content = request.get_json(silent=True)
    if content == None:
        return {'status' : 'fail', 'message': 'Validation failed'}, 400
    #validacja!!
    user = User(content)
    repo = UserRepository(getDb())
    repo.update(user)

    return '', 204


@app.route("/<username>/activate/<code>", methods=['PATCH'])
def activate(username, code):
    repo = UserRepository(getDb())
    user = repo.findByUsername(username)
    if user.activationCode != code:
        return {'status' : 'fail', 'message': 'zly kod aktywacyjny'}, 400

    user.activationCode = None
    user.isEnabled = True

    #wyslac email ze gitowo!
    repo.update(user)

    return '', 204

@is_logged
@app.route("", methods=['GET'], defaults={'username': None})
@app.route("/<username>", methods=['GET'])
def getUser(user: User, username: str):
    if username == None:
        return {'status' : 'ok', 'data': user.toDict()}, 200
    elif user.hasRole('admin') and username != None:
        repo = UserRepository(getDb())
        user = repo.findByUsername(username)
        if user:
            return {'status' : 'ok', 'data': user.toDict()}, 200
    else:
        return {'status' : 'fail', 'message': 'Forbidden'}, 403

@is_logged
@app.route("/", methods=['DELETE'])
@app.route("/<username>", methods=['DELETE'])
def deleteUser(user: User, username: str):
    if username == None:
        pass
    elif user.hasRole('admin') and username != None:
        repo = UserRepository(getDb())
        user = repo.findByUsername(username)
        if user:
            return {'status' : 'ok', 'data': user.toDict()}, 200
        else:
            return {'status' : 'fail', 'message': 'User not found'}, 400
    else:
        return {'status' : 'fail', 'message': 'Forbidden'}, 403
    
    repo = UserRepository(getDb())
    try:
        repo.remove(user.id())
    except Exception as e:
        current_app.logger.error(e)
        return {'status' : 'fail', 'message': 'Error during deletion'}, 500
    return '', 204