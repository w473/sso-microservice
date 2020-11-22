from .AbstractRepository import AbstractRepository
from bson.objectid import ObjectId
from ..documents.RefreshToken import RefreshToken
from ..documents.User import User
from flask import current_app
import logging
logger = logging.getLogger( __name__ )

class RefreshTokenRepository(AbstractRepository):
    def save(self, refreshToken : RefreshToken) -> None:
        """
        docstring
        """
        self.client.refreshToken.insert_one(
            refreshToken.toDict()
        )

    def exist(self, token: str, userId: str) -> bool:
        doc = self.client.refreshToken.find_one({"_id": token, "userId" : userId})
        if doc != None:
            return True
        return False

    def delete(self, token: str) -> None:
        self.client.refreshToken.delete_one({"_id": token})

    def findByUser(self, user: User) -> list:
        docs = self.client.refreshToken.find({"userId": ObjectId(user.id)})
        ret = []
        for doc in docs:
            ret.append(RefreshToken(doc['token'], doc['_id']))
        
        return ret