from flask import Flask
from flaskr.services.RequestService import Request
import json


class NewRequestObject(Request):
    def __init__(self, message, payload, code=200):
        self.message = message
        self.payload = payload
        self.code = code

    def post(self, url, jsonPayload, headers):
        return Response(self.code, {"message": self.message, "data": self.payload})


class Response():
    def __init__(self, status_code, json):
        self.status_code = status_code
        self._json = json

    def json(self):
        return self._json


def setUserAdmin(app: Flask) -> None:
    app.services['request'] = NewRequestObject(
        '342134234', {"id": "4efe5012-8f81-400b-a915-01c5187e082f", "email": 'email@asd.de', "roles": ['USER', 'ADMIN']})


def setUserNormal(app: Flask) -> None:
    app.services['request'] = NewRequestObject(
        'aaaa', {"id": "bc41951c-0538-4626-8067-ccf6570edcfe", "email": 'email@ddd.de', "roles": ['USER']})


def setUserNotActive(app: Flask) -> None:
    app.services['request'] = NewRequestObject(
        'aaaa', {"id": "bc41951c-0538-4626-8067-ccf6570edcfe", "email": 'email@ddd.de', "roles": ['USER'], "isActive": False})


def setUserNotFound(app: Flask) -> None:
    app.services['request'] = NewRequestObject(
        'aaaa', {}, 403)


def jsonCompareDict(jsonBytes, dictToCompare):
    jsonDict = json.loads(jsonBytes)
    for key, value in dictToCompare.items():
        assert jsonDict.get(key) == value
