from flask import Blueprint, request, current_app, url_for
from pymongo.errors import DuplicateKeyError
from datetime import datetime
from passlib.hash import sha256_crypt
from flaskr.domain.documents.User import User
from flaskr.domain.repositories.UserRepository import UserRepository 
from flaskr.domain.mongo import getDb, DbClient
from flaskr.formatters.UserFormatter import forApiAsDict
from flaskr.services import AuthService, RequestService, EmailService

import logging
logger = logging.getLogger( __name__ )

app = Blueprint('user', __name__, url_prefix='/user')

@app.route("", methods=['POST'])
@RequestService.validate(kind='user_create')
def create():
    content = request.get_json(silent=True)
    if content == None:
        return {'message': 'Invalid Request'}, 400

    user = User(content)
    try:
        user.setCreate(datetime.utcnow())
        user.setActive(False)
        password = sha256_crypt.encrypt(content.get('password'))
        user.setPassword(password)
        repo = UserRepository(getDb())

        emailService = EmailService.getEmailService()
        activationUrl = current_app.config['BASE_URL'] + url_for(
            'user.activate', 
            username=user.username, 
            code=user.activationCode
        )

        contents = emailService.prepareContents(
            'activation', 
            user.locale, 
            name=user.name,
            url=activationUrl
        )
        emailService.sendEmail(user.name, user.email, contents)    
        
        repo.add(user)

    except DuplicateKeyError as e:
        keyColumn = list(e.details.get('keyPattern').keys())[0]
        if keyColumn == 'username':
            return {'message': 'Please choose different username'}, 400
        elif keyColumn == 'email':
            return {'message': 'You cannot use this email address'}, 400
        else:
            raise Exception('Unknown column key raised error : "'+keyColumn+'"')
        return {'message': 'User already exists! - this error should not be here'}, 400

    return '', 204

@app.route("", methods=['PATCH'], defaults={'username': None})
@app.route("/<username>", methods=['PATCH'])
@RequestService.validate(kind='user_update')
@AuthService.is_logged
def update(user: User, username: str):
    repo = UserRepository(getDb())
    if username == None:
        pass
    elif user.hasRole('admin') and username != None:
        user = repo.findByUsername(username)
        if user == None:
            return {'message': 'User not found'}, 400
    else:
        return {'message': 'Forbidden'}, 403

    content = request.get_json(silent=True)
    if content == None:
        return {'message': 'Validation failed'}, 400

    try:
        if content.get('password'):
            content['password'] = sha256_crypt.encrypt(content.get('password'))
        repo = UserRepository(getDb())
        newUser = User(content)
        hasNewEmail = False
        if content.get('email') and user.email != content.get('email'):
            newUser.setActive(False)
            hasNewEmail = True
        repo.update(newUser)
        if hasNewEmail:
            return {'message': 'Please activate your email'}, 200
        else:
            return '', 204
    except DuplicateKeyError as e:
        keyColumn = list(e.details.get('keyPattern').keys())[0]
        if keyColumn == 'username':
            return {'message': 'Please choose different username'}, 400
        elif keyColumn == 'email':
            return {'message': 'You cannot use this email address'}, 400
        else:
            raise Exception('Unknown column key raised error : "'+keyColumn+'"')
        return {'message': 'User already exists! - this error should not be here'}, 400
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

@AuthService.is_logged
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

@AuthService.is_logged
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