from flask import Blueprint, abort
from jwcrypto.jwk import JWK, JWKSet
from ..services.KeyService import KeyService
from ..domain.repositories.KeyRepository import KeyRepository
from ..domain.repositories.AbstractRepository import DBException
from ..domain.db import getDb
from ..formatters.KeyFormatter import forApiAsDict
from flaskr.services.AuthService import is_logged
import base64
import logging
logger = logging.getLogger(__name__)

controller = Blueprint('key', __name__)


@controller.route("/key/generate", methods=['PUT'], endpoint='generate')
@is_logged(role='ADMIN')
def newKeyGenerate():
    generate()
    return '', 204


@controller.route("/key/<id>", methods=['GET'], endpoint='get')
@is_logged(role='ADMIN')
def get(id):
    repo = KeyRepository(getDb())
    try:
        key = repo.findOne(id)
    except DBException:
        return {'message': 'Key id is invalid'}, 400

    if key == None:
        return {'message': 'Key has not been found'}, 404
    else:
        return base64.b64decode(key.publicKey)


@controller.route("/key/<id>", methods=['DELETE'], endpoint='delete')
@is_logged(role='ADMIN')
def delete(id):
    repo = KeyRepository(getDb())
    try:
        if repo.delete(id):
            return '', 204
        else:
            return {'message': 'Key has not been found'}, 404
    except DBException:
        return {'message': 'Key id is invalid'}, 400


@controller.route("/key", methods=['GET'], endpoint='listAll')
@controller.route("/.well-known/jwks.json", methods=['GET'], endpoint='listAllJWK')
def listAll():
    repo = KeyRepository(getDb())
    docList = repo.fetchAll()

    jwkset = JWKSet()
    for keyDoc in docList:
        jwk = JWK.from_pem(base64.b64decode(keyDoc.publicKey))
        # wrong way, no idea how to make it proper :|
        jwk._params['kid'] = str(keyDoc.id)
        jwk._params['alg'] = keyDoc.algorithm

        jwkset.add(jwk)

    return jwkset.export(private_keys=False, as_dict=True)


@ controller.cli.command('generate')
def newKeyGenerateCli():
    generate()


def generate() -> None:
    service = KeyService()
    key = service.generate()
    service.save(key)
