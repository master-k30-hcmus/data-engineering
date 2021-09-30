from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from . import config


class MongoDB:
    def __init__(self, db_name: str):
        client = MongoClient(config["MONGO_URI"])
        if not client:
            print("Cannot create connection to MongoDB.")
            exit(0)
        self.client = client
        self.db = client[db_name]

    def get_client(self):
        return self.client

    def get_database(self) -> Database:
        return self.db

    def get_collection(self, coll_name: str) -> Collection:
        return self.db[coll_name]

    def close(self):
        self.client.close()
