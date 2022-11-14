import os

import pymongo
from pymongo.collection import Collection


def get_mongo_collection(db_name: str, coll_name: str, conn_str=None) -> Collection:
    conn_str = conn_str or os.environ["MONGO_CONN_STR"]
    client = pymongo.MongoClient(conn_str)
    return client[db_name][coll_name]
