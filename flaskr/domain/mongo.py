from flask import current_app
from pymongo import MongoClient, database

def getDb() -> database.Database:
    if current_app.db == None:
        raise Exception('DB connection has not been initialized')
    return current_app.db

def DbClient() -> MongoClient:
    if current_app.dbClient == None:
        raise Exception('DB connection has not been initialized')
    return current_app.dbClient

def setDb(app, url: str, username: str, password: str, authSource: str, database: str) -> None:
    app.dbClient = MongoClient(url,username=username, password=password, authSource=authSource)
    app.db = app.dbClient[database]