from pymongo import MongoClient

class AbstractRepository:
    client = None

    def __init__(self, client: MongoClient):
        self.client = client