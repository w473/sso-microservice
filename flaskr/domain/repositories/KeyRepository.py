from flaskr.domain.repositories.AbstractRepository import AbstractRepository
from flaskr.domain.documents.Key import Key as KeyDocument
from flask import current_app
from pymysql.connections import Connection


class KeyRepository(AbstractRepository):
    def __init__(self, connection: Connection) -> None:
        super().__init__(connection, 'securityKey')

    def save(self, key: KeyDocument):
        """
        docstring
        """
        id = self.insertOne(key.toDict())
        key.setId(id)

    def findOne(self, id) -> KeyDocument:
        doc = self.findOneBy({'id': id})
        if doc != None:
            return KeyDocument(doc['publicKey'], doc['privateKey'], doc['algorithm'], doc['id'])

        return None

    def findRandom(self) -> KeyDocument:
        doc = self.findOneRandom()
        if doc != None:
            return KeyDocument(doc['publicKey'], doc['privateKey'], doc['algorithm'], doc['id'])

        return None

    def fetchAll(self):
        ret = []
        for doc in self.findAllBy(dict()):
            keyDoc = KeyDocument(
                doc['publicKey'], doc['privateKey'], doc['algorithm'], doc['id'])
            ret.append(keyDoc)
        return ret

    def delete(self, id) -> bool:
        return self.deleteBy({'id': id}) == 1
