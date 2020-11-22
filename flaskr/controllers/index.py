from flask import Blueprint, abort

app = Blueprint('index', __name__)

@app.route("/")
def index():
    return "Welcome to Trakayo SSO"