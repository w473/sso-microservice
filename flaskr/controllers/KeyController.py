from flask import Blueprint, abort
from ..services.KeyService import KeyService
from ..domain.repositories.KeyRepository import KeyRepository 
from ..domain.mongo import getDb
from ..formatters.KeyFormatter import forApiAsDict
from flaskr.services.AuthService import is_logged
from pymongo.errors import InvalidId

import logging
logger = logging.getLogger( __name__ )

controller = Blueprint('key', __name__, url_prefix='/key')

@controller.route("/generate", methods=['PUT'], endpoint='generate')
@is_logged(role='ADMIN')
def neweKeyGenerate():
    generate()
    return '', 204

@controller.route("/<id>", methods=['GET'], endpoint='get')
@is_logged(role='ADMIN')
def get(id):
    repo = KeyRepository(getDb())
    try:
        key = repo.findOne(id)
    except InvalidId:
        return {'message':'Key id is invalid'}, 400
    
    if key == None:
        return {'message':'Key has not been found'}, 404
    else:
        return key.publicKey

@controller.route("/<id>", methods=['DELETE'], endpoint='delete')
@is_logged(role='ADMIN')
def delete(id):
    repo = KeyRepository(getDb())
    try:
        if repo.delete(id): 
            return '', 204
        else:
            return {'message':'Key has not been found'}, 404
    except InvalidId:
        return {'message':'Key id is invalid'}, 400

@controller.route("", methods=['GET'], endpoint='listAll')
@is_logged(role='ADMIN')
def listAll():
    repo = KeyRepository(getDb())
    docList = repo.fetchAll()
    return forApiAsDict(docList)

@controller.cli.command('generate')
def newKeyGenerateCli():
    generate()

def generate() -> None:
    service = KeyService()
    key = service.generate()
    service.save(key)