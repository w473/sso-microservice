from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from ..domain.documents.Key import Key as KeyDocument
from ..domain.repositories.KeyRepository import KeyRepository
from ..domain.db import getDb
import base64


class KeyService:
    def generate(self):
        keyBytes = 512
        key = RSA.generate(keyBytes*8)
        return KeyDocument(
            base64.b64encode(key.publickey().exportKey('PEM')),
            base64.b64encode(key.exportKey('PEM')),
            'RS'+str(keyBytes)
        )

    def save(self, keyDocument):
        repo = KeyRepository(getDb())
        repo.save(keyDocument)
