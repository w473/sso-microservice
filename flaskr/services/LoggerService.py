import logging
from flask import Flask
from flask_graylog import Graylog


def initLogger(app: Flask):
    graylog = Graylog(app)
    app.logger.addHandler(graylog.handler)
