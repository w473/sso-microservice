from .AbstractRepository import AbstractRepository
from ..documents.RefreshToken import RefreshToken
from ..documents.User import User
from flask import current_app
from pymysql.connections import Connection
import uuid
import logging
logger = logging.getLogger(__name__)


class RefreshTokenRepository(AbstractRepository):
    def __init__(self, connection: Connection) -> None:
        super().__init__(connection, 'refreshToken')

    def save(self, refreshToken: RefreshToken) -> None:
        """
        docstring
        """
        self.insertOne(
            {
                'token': uuid.UUID(refreshToken.token).bytes,
                'userId': uuid.UUID(refreshToken.userId).bytes,
            }
        )

    def exist(self, token: str, userId: str) -> bool:
        doc = self.findOneBy(
            {
                "token": uuid.UUID(token).bytes,
                "userId": uuid.UUID(userId).bytes
            }
        )
        if doc != None:
            return True
        return False

    def delete(self, token: str) -> None:
        self.deleteBy({"token": uuid.UUID(token).bytes})

    def deleteForUser(self, userId: str) -> None:
        self.deleteBy({"userId": uuid.UUID((userId)).bytes})

    def findByUser(self, userId: uuid) -> list:
        docs = self.findAllBy({"userId": uuid.UUID((userId).bytes)})
        ret = []
        for doc in docs:
            ret.append(
                RefreshToken(
                    uuid.UUID(doc['token']).hex,
                    uuid.UUID(doc['token']).hex
                )
            )

        return ret
