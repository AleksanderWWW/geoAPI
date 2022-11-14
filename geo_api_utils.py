import pymongo
from pymongo.collection import Collection


def get_mongo_collection(conn_str: str, db_name: str, coll_name: str) -> Collection:
    client = pymongo.MongoClient(conn_str)
    return client[db_name][coll_name]