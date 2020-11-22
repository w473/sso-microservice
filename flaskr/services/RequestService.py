from flask import g, current_app, request
from functools import wraps
import logging
import os
import json
from jsonschema import validate as jsonValidate, Draft7Validator, FormatChecker
from collections import deque

logger = logging.getLogger( __name__ ) 

def get_schema( kind, operation='default' ):
    try:
        path = current_app.config['VALIDATION_SCHEMAS_PATH']
        path = os.path.join( path, '{0}.json'.format( kind ) )
        logger.info( 'Reading schema from {0}'.format( path ) )
        with open( path ) as file:
            return json.load( file )
    except:
        raise JSONSchemaValidatorException( "The validation schema "+path+" or operation could not be found" )

def validate(kind, operation='default', root=None ):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            schema = get_schema( kind, operation )
            if schema is None:
                raise JSONSchemaValidatorException( "The validation schema kind or operation could not be found" )
            validator = Draft7Validator(schema)
            errors = {}
            for error in validator.iter_errors(request.json):
                errors[''.join(error.path)] = error.message
            if len(errors) > 0:
                raise JSONSchemaValidatorFailException(errors)
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

# def printDeque(queue:deque) -> str:
#     ret = '';
#     for elem in queue:
#         ret
#         print(elem.upper())



class JSONSchemaValidatorException( Exception ):
    pass

class JSONSchemaValidatorFailException( Exception ):
    def __init__(self, errors: dict):
        self.errors = errors