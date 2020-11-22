import jwt
from ..domain.mongo import getDb
from ..domain.repositories.KeyRepository import KeyRepository
from datetime import timedelta, datetime
from flask import current_app
from Crypto.PublicKey import RSA
import base64 
from flask import g, current_app, Request

def encodeJwt(payload:dict) -> str:
    payload['exp'] = (datetime.utcnow() + timedelta(minutes=3))
    repo = KeyRepository(getDb())
    key = repo.findRandom()
    if key == None:
        raise Exception('Key collection seems to be empty!')
    
    return jwt.encode(
        payload,
        key.privateKey, 
        algorithm=key.algorithm, 
        headers={'kid': str(key.id)}
        )

def decodeJwt(jwtString:str, notAllowExpired: bool = True) -> dict:
    headers = jwt.get_unverified_header(jwtString)
    kid = headers.get('kid')
    if kid == None:
        raise Exception('JWT invalid - kid not found')
    
    repo = KeyRepository(getDb())
    key = repo.findOne(kid)
    if key == None:
        raise Exception('JWT invalid - key with kid '+ kid +' does not exists')
    return jwt.decode(jwtString, key.publicKey, algorithms=key.algorithm, verify_expiration = notAllowExpired)    
    