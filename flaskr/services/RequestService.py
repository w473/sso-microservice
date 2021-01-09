from flask import g, current_app, request
from functools import wraps
import logging
import os
import json
import requests
from jsonschema import validate as jsonValidate, Draft7Validator, FormatChecker
from collections import deque

logger = logging.getLogger(__name__)


def get_schema(kind, operation='default'):
    try:
        path = current_app.config['VALIDATION_SCHEMAS_PATH']
        path = os.path.join(path, '{0}.json'.format(kind))
        logger.info('Reading schema from {0}'.format(path))
        with open(path) as file:
            return json.load(file)
    except:
        raise JSONSchemaValidatorException(
            "The validation schema "+path+" or operation could not be found")


def validate(kind: str, operation: str = 'default'):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            validateDict(request.json, kind, operation)
            return f(*args, **kwargs)
        return wrapper
    return decorator


def validateDict(dict: dict, kind: str, operation: str = 'default'):
    schema = get_schema(kind, operation)
    if schema is None:
        raise JSONSchemaValidatorException(
            "The validation schema kind or operation could not be found")
    validator = Draft7Validator(schema)
    errors = {}
    for error in validator.iter_errors(dict):
        path = '.'.join(map(str, error.path))
        errors[path] = error.message
    if len(errors) > 0:
        raise JSONSchemaValidatorFailException(errors)


class Request ():
    def post(self, url, jsonPayload, headers):
        return requests.post(url, json=jsonPayload, headers=headers)


def getRequest() -> Request:
    if not 'request' in current_app.services:
        setRequest(Request())
    return current_app.services['request']


def setRequest(newRequestObject) -> None:
    current_app.services['request'] = newRequestObject


class JSONSchemaValidatorException(Exception):
    pass


class JSONSchemaValidatorFailException(Exception):
    def __init__(self, errors: dict):
        self.errors = errors
