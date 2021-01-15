import base64
from ..domain.db import getDb
from ..domain.repositories.KeyRepository import KeyRepository
from datetime import timedelta, datetime
from flask import current_app
from Crypto.PublicKey import RSA
from flask import g, current_app, Request
import base64
import json
import time
from jwcrypto import jwt, jwk


def encodeJwt(payload: dict) -> str:
    payload['exp'] = (time.time() + 60*3)
    repo = KeyRepository(getDb())
    key = repo.findRandom()
    if key == None:
        raise Exception('Key collection seems to be empty!')

    keyBytes = key.privateKey

    keyDecoded = jwk.JWK.from_pem(base64.b64decode(keyBytes))

    Token = jwt.JWT(
        header={"alg": key.algorithm, 'kid': str(key.id)},
        claims=payload
    )
    Token.make_signed_token(keyDecoded)

    return Token.serialize()


def decodeJwt(jwtString: str) -> dict:
    ET = jwt.JWT()
    ET.deserialize(jwtString)

    kid = ET.token.jose_header.get('kid')
    if kid == None:
        raise Exception('JWT invalid - kid not found')

    repo = KeyRepository(getDb())
    key = repo.findOne(kid)
    if key == None:
        raise Exception('JWT invalid - key with kid ' +
                        kid + ' does not exists')

    keyBytes = key.publicKey.encode('ascii')
    keyDecoded = jwk.JWK.from_pem(base64.b64decode(keyBytes))

    payload = json.loads(ET.token.objects.get('payload'))

    try:
        ET.deserialize(jwtString, keyDecoded)
    except jwt.JWTExpired as e:
        raise JWTExpiredException(e, payload)

    return payload


class JWTExpiredException(Exception):
    def __init__(self, previous, payload):
        self.previous = previous
        self.payload = payload
