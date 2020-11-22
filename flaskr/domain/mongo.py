from flask import g
from pymongo import MongoClient

def getDb():
    if 'db' not in g:
        client = MongoClient('mongodb://localhost:27017/',username="user", password="pass", authSource='admin')
        g.db = client.trakayo
    return g.db
