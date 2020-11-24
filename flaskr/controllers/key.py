from flask import Blueprint, abort
from ..services.KeyService import KeyService
from ..domain.repositories.KeyRepository import KeyRepository 
from ..domain.mongo import getDb
from ..formatters.KeyFormatter import forApiAsDict
from flaskr.services.AuthService import is_logged

app = Blueprint('key', __name__, url_prefix='/key')

@app.route("/generate", methods=['PUT'], endpoint='generate')
@is_logged(role='ADMIN')
def generate():
    service = KeyService()
    key = service.generate()
    service.save(key)
    return '', 204

@app.route("/<id>", methods=['GET'], endpoint='get')
@is_logged(role='ADMIN')
def get(id):
    repo = KeyRepository(getDb())
    return repo.findOne(id).publicKey

@app.route("/", methods=['GET'], endpoint='listAll')
@is_logged(role='ADMIN')
def listAll():
    repo = KeyRepository(getDb())
    docList = repo.fetchAll()
    return forApiAsDict(docList)