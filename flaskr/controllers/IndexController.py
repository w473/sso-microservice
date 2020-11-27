from flask import Blueprint, abort

controller = Blueprint('index', __name__)

@controller.route("/")
def index():
    return "Welcome to Trakayo SSO"