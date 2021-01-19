import os
from flask import Flask
from flaskr.services.RequestService import JSONSchemaValidatorFailException
from flaskr.domain import db
from flaskr.services.AppsAuthorizationService import parseConfig
from flaskr.services.LoggerService import initLogger
import jsonschema
import sys
import traceback
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv
from flaskr.services.OpenapiService import openAPI


def create_app(config=None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if config == None:
        load_dotenv(dotenv_path='../.env')
        config = os.environ
    app.config['USERS_SERVICE_URL'] = config.get('USERS_SERVICE_URL')
    app.config['DB_HOSTNAME'] = config.get('DB_HOSTNAME')
    app.config['DB_USERNAME'] = config.get('DB_USERNAME')
    app.config['DB_PASSWORD'] = config.get('DB_PASSWORD')

    app.config['GRAYLOG_HOST'] = config.get('GRAYLOG_HOST')
    app.config['GRAYLOG_FACILITY'] = 'sso'

    app.config['DB_NAME'] = config.get('DB_NAME')
    app.config['APPS_CREDENTIALS'] = parseConfig(
        config.get('APPS_CREDENTIALS')
    )
    app.config['VALIDATION_SCHEMAS_PATH'] = "flaskr/resources/validation_schemas"
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    initLogger(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from flaskr.controllers import IndexController, KeyController, AuthController

    app.register_blueprint(IndexController.controller)
    app.register_blueprint(KeyController.controller)
    app.register_blueprint(AuthController.controller)

    # placeholder for services that could be exchanged
    app.services = dict()

    from flaskr.commands import InitCommand
    app.register_blueprint(InitCommand.command)

    openAPI(app)

    @ app.errorhandler(JSONSchemaValidatorFailException)
    def onValidationError(e):
        return {'message': 'Validation failed', 'data': e.errors}, 400

    @ app.errorhandler(Exception)
    def onException(e):
        if issubclass(e.__class__, HTTPException):
            return e.get_response()
        app.log_exception(e)
        return {'message': 'Unexpected error occured'}, 500

    @ app.teardown_appcontext
    def closeDb(error):
        if error:
            app.logger.error(error)
        db.closeDb()

    return app
