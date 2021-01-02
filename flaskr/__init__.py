import os
from flask import Flask
from flaskr.services.RequestService import JSONSchemaValidatorFailException
from flaskr.domain import mongo
from flaskr.services import EmailService
import jsonschema
import logging
logger = logging.getLogger(__name__)


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        VALIDATION_SCHEMAS_PATH="flaskr/resources/validation_schemas",
        MAILING_TEMPLATES_PATH="flaskr/resources/email_templates"
    )

    mongo.setDb(
        app,
        os.environ.get('MONGO_URL'),
        os.environ.get('MONGO_USERNAME'),
        os.environ.get('MONGO_PASSWORD'),
        os.environ.get('MONGO_AUTH_SOURCE'),
        os.environ.get('MONGO_DATABASE')
    )

    EmailService.setEmailService(
        app,
        False,
        os.environ.get('MAILING_SMTP_SERVER'),
        os.environ.get('MAILING_SMTP_PORT'),
        os.environ.get('MAILING_SENDER'),
        os.environ.get('MAILING_SENDER_EMAIL'),
        os.environ.get('MAILING_SMTP_PASSWORD'),
        os.environ.get('MAILING_TEMPLATES_PATH')
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from flaskr.controllers import IndexController, UserController, KeyController, AuthController

    app.register_blueprint(IndexController.controller)
    app.register_blueprint(UserController.controller)
    app.register_blueprint(KeyController.controller)
    app.register_blueprint(AuthController.controller)

    from flaskr.commands import InitCommand
    app.register_blueprint(InitCommand.command)

    @app.errorhandler(JSONSchemaValidatorFailException)
    def onValidationError(e):
        logger.info(e)
        return {'data': e.errors}, 400

    @app.errorhandler(Exception)
    def onException(e):
        logger.error(e)
        return {'data': 'Unexpected error occured'}, 500

    return app
