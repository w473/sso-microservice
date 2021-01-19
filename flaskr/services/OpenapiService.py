
from flasgger import Swagger


def openAPI(app):

    app.config['SWAGGER'] = {
        'openapi': '3.0.1',
        "title": "SSO",
        "specs_route": "/api-docs/",
        "headers": [
        ],
        "specs": [
            {
                "version": "1.0.0",
                "title": "SSO",
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "description": 'This is the version 1 of our API',
            }
        ]
    }

    Swagger(app)
