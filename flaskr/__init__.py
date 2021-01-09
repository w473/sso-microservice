import os
from flask import Flask
from flaskr.services.RequestService import JSONSchemaValidatorFailException
from flaskr.domain import db
import jsonschema
import logging
import sys
import traceback

logger = logging.getLogger(__name__)


def create_app(config=None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if config == None:
        config = os.environ
    app.config['USERS_SERVICE_URL'] = config.get('USERS_SERVICE_URL')
    app.config['DB_HOSTNAME'] = config.get('DB_HOSTNAME')
    app.config['DB_USERNAME'] = config.get('DB_USERNAME')
    app.config['DB_PASSWORD'] = config.get('DB_PASSWORD')
    app.config['DB_NAME'] = config.get('DB_NAME')

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

    @app.errorhandler(JSONSchemaValidatorFailException)
    def onValidationError(e):
        logger.info(e)
        return {'data': e.errors}, 400

    @app.errorhandler(Exception)
    def onException(e):
        exc_type, exc_value, exc_traceback = sys.exc_info()

        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)

        logger.error(print(repr(traceback.format_exception(exc_type, exc_value,
                                                           exc_traceback))))
        return {'data': 'Unexpected error occured'}, 500

    @app.teardown_appcontext
    def closeDb(error):
        db.closeDb(error)

    return app
