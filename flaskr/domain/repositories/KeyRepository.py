from .AbstractRepository import AbstractRepository
from ..documents.Key import Key as KeyDocument
from bson.objectid import ObjectId
from flask import current_app

class KeyRepository(AbstractRepository):
    def save(self, key: KeyDocument):
        """
        docstring
        """
        id = self.client.securityKey.insert_one(key.toDict()).inserted_id
        key.setId(id)
    
    def findOne(self, id) -> KeyDocument:
        doc = self.client.securityKey.find_one({"_id": ObjectId(id)})
        if doc != None:
            return KeyDocument(doc['publicKey'], doc['privateKey'], doc['algorithm'], doc['_id'])
        
        return None
        
    def findRandom(self) -> KeyDocument:
        doc = self.client.securityKey.aggregate([{ '$sample': { 'size': 1 } }]).next()
        if doc != None:
            return KeyDocument(doc['publicKey'], doc['privateKey'], doc['algorithm'], doc['_id'])
        
        return None

    def fetchAll(self):
        ret = []
        for doc in self.client.securityKey.find():
            keyDoc = KeyDocument(doc['publicKey'], doc['privateKey'], doc['algorithm'], doc['_id'])
            ret.append(keyDoc)
        return ret
    
    def delete(self, id) -> bool:
        return self.client.securityKey.delete_one({"_id": ObjectId(id)}).deleted_count == 1

