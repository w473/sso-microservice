from jwcrypto import jwk
from ..domain.documents.Key import Key as KeyDocument
from ..domain.repositories.KeyRepository import KeyRepository
from ..domain.db import getDb
import base64


class KeyService:
    def generate(self):
        keyBytes = 512
        key = jwk.JWK.generate(kty='RSA', size=keyBytes*8)

        return KeyDocument(
            base64.b64encode(key.export_to_pem(False, None)),
            base64.b64encode(key.export_to_pem(True, None)),
            'RS'+str(keyBytes)
        )

    def save(self, keyDocument):
        repo = KeyRepository(getDb())
        repo.save(keyDocument)
