from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from ..domain.documents.Key import Key as KeyDocument
from ..domain.repositories.KeyRepository import KeyRepository 
from ..domain.mongo import getDb

class KeyService:
    def generate(self):
        keyBytes = 512
        key = RSA.generate(keyBytes*8)
        return KeyDocument(
            key.publickey().exportKey('PEM'),
            key.exportKey('PEM'),
            'RS'+str(keyBytes)
        )
    
    def save(self, keyDocument):
        repo = KeyRepository(getDb())
        repo.save(keyDocument)

