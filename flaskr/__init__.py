import os

from flask import Flask
from flaskr.services.RequestService import JSONSchemaValidatorFailException
from flaskr.domain import mongo
from flaskr.services import EmailService

import logging
logger = logging.getLogger( __name__ )

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        VALIDATION_SCHEMAS_PATH="flaskr/resources/validation_schemas",
        MAILING_TEMPLATES_PATH="flaskr/resources/email_templates"
        # store the database in the instance folder
        # DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_json("config.json", silent=False)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    mongo.setDb(
        app, 
        app.config['MONGO_URL'], 
        app.config['MONGO_USERNAME'], 
        app.config['MONGO_PASSWORD'], 
        app.config['MONGO_AUTH_SOURCE'], 
        app.config['MONGO_DATABASE']
    )

    EmailService.setEmailService(
        app, 
        test_config is None, 
        app.config['MAILING_SMTP_SERVER'], 
        app.config['MAILING_SMTP_PORT'], 
        app.config['MAILING_SENDER'], 
        app.config['MAILING_SENDER_EMAIL'], 
        app.config['MAILING_SMTP_PASSWORD'], 
        app.config['MAILING_TEMPLATES_PATH']
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # # register the database commands
    # from flaskr import db

    # db.init_app(app)
    import jsonschema

    # apply the blueprints to the app
    from flaskr.controllers import IndexController, UserController, KeyController, AuthController

    app.register_blueprint(IndexController.controller)
    app.register_blueprint(UserController.controller)
    app.register_blueprint(KeyController.controller)
    app.register_blueprint(AuthController.controller)


    @app.errorhandler( JSONSchemaValidatorFailException )
    def onValidationError( e ):
        logger.info(e)
        return { 'data' : e.errors }, 400
    
    @app.errorhandler( Exception )
    def onException( e ):
        logger.error(e)
        return { 'data' : 'Unexpected error occured' }, 500

    return app