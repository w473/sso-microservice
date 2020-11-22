from .AbstractRepository import AbstractRepository
from ..documents.User import User as UserDocument
from bson.objectid import ObjectId

class UserRepository(AbstractRepository):
    def add(self, user: UserDocument):
        """
        docstring
        """
        id = self.client.user.insert_one(user.toDict()).inserted_id
        user.setId(id)

    def update(self, user: UserDocument):
        """
        docstring
        """
        self.client.user.replace_one(user.toDict())
    
    def findOne(self, userId):
        doc = self.client.user.find_one({"_id": ObjectId(userId)})
        if doc != None:
            return UserDocument(doc)
        
        return None

    def remove(self, userId):
        self.client.user.delete_one({"_id": ObjectId(userId)})

    def findByUsername(self, username: str) -> UserDocument:
        doc = self.client.user.find_one({'username': username})

        if doc != None:
            return UserDocument(doc, doc.get('_id'))
        
        return None
