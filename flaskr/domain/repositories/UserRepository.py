from .AbstractRepository import AbstractRepository
from ..documents.User import User as UserDocument
from bson.objectid import ObjectId
import logging

logger = logging.getLogger( __name__ )
class UserRepository(AbstractRepository):
    def add(self, user: UserDocument, **kwargs):
        """
        docstring
        """
        id = self.client.user.insert_one(user.toDict(), **kwargs).inserted_id
        user.setId(id)

    def update(self, user: UserDocument):
        """
        docstring
        """
        logger.error(user.toDict())
        logger.error(user.id)
        logger.error({"_id": ObjectId(user.id)})
        a = self.client.user.replace_one({"_id": ObjectId(user.id)}, user.toDict())
        logger.error(a)
    
    def findOne(self, userId):
        doc = self.client.user.find_one({"_id": ObjectId(userId)})
        if doc != None:
            return UserDocument(doc)
        
        return None

    def delete(self, userId):
        self.client.user.delete_one({"_id": ObjectId(userId)})

    def findByUsername(self, username: str) -> UserDocument:
        doc = self.client.user.find_one({'username': username})

        if doc != None:
            ret = UserDocument(doc, doc.get('_id'))
            ret.setRoles(doc.get('roles'))
            return ret
        
        return None
