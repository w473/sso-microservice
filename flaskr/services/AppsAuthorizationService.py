import json
import base64
from flask import current_app
import bcrypt


def parseConfig(config: str) -> dict:
    if len(config) == 0:
        raise Exception('APPS_CREDENTIALS is empty')

    config = json.loads(config)
    ret = dict()
    for key, val in config.items():
        ret[key] = base64.b64decode(val)

    return ret


def isAppCredentialValid(app, key) -> bool:
    hashedAppKey = current_app.config['APPS_CREDENTIALS'].get(app)
    if hashedAppKey:
        return bcrypt.checkpw(key.encode(), hashedAppKey)
    return False
