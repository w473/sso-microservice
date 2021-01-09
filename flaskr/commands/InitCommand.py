from flask import Blueprint
from flaskr.domain.db import initDb

command = Blueprint('init', __name__)


@command.cli.command('db')
def initDB():
    initDb()
