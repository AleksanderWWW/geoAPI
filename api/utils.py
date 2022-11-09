from typing import (
    Any,
    Dict,
    Tuple,
)

import pymongo
import requests
from flask import Request
from pymongo.collection import Collection
from pymongo.errors import (
    CollectionInvalid,
    DocumentTooLarge,
    ExecutionTimeout,
)


def parse_request(request: Request) -> str:
    if "ip" in request.args.keys():
        ip = request.args.get("ip")
    elif "ip" in request.json.keys():
        ip = request.json.get("ip")
    else:
        ip = ""

    return ip


def fetch_ip_data(ip: str, ip_stack_key: str) -> Dict[str, Any]:
    """
    Fetches json response from ipstack API about a particular ip address

    :param ip: ip address of interest
    :type ip: str
    :param ip_stack_key: api key necessary to access ipstack API
    :type ip_stack_key: str

    :return: json response from ipstack API
    :rtype: dict
    """
    url = f"http://api.ipstack.com/{ip}?access_key={ip_stack_key}"
    resp = requests.get(url)
    return resp.json()


def get_mongo_collection(conn_str: str, db_name: str, coll_name: str) -> Collection:
    client = pymongo.MongoClient(conn_str)
    return client[db_name][coll_name]


def verify_user(username: str, password: str, users: Collection) -> bool:
    query = {"username": username}
    res = users.find(query)
    try:
        user = res.next()
    except StopIteration:  # wrong username
        return False

    if user["password"] == password:
        return True

    # wrong password
    return False


def retrieve_ip_data(ip: str, collection: Collection) -> Dict[str, Any]:
    query = {"ip": ip}
    res = collection.find(query, {"_id": 0})

    try:
        data = res.next()
        return data
    except StopIteration:  # no result in database
        return {}


def save_ip_data(data: Dict[str, Any], collection: Collection) -> Tuple[Dict[str, str], int]:
    response = {"msg": ""}
    # check if ip already in database
    ip = data["ip"]
    if collection.count_documents({"ip": ip}):
        response["msg"] = f"Data for ip {ip} already present"
        code = 200
    else:
        try:
            collection.insert_one(data)
            response["msg"] = "Insertion successful"
            code = 200
        except DocumentTooLarge:
            response["msg"] = "Document provided was to large"
            code = 400
        except ExecutionTimeout:
            response["msg"] = "Execution timed out"
            code = 408
        except CollectionInvalid:
            response["msg"] = "Chosen collection is invalid"
            code = 404

    return response, code


def delete_ip_data(ip: str, collection: Collection) -> Tuple[Dict[str, str], int]:
    query = {"ip": ip}
    response = {"msg": ""}

    collection.delete_one(query)
    response["msg"] = "Deletion successful"
    return response, 200
