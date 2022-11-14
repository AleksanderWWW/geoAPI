from typing import (
    Any,
    Dict,
    Tuple,
)

from pymongo.errors import (
    CollectionInvalid,
    DocumentTooLarge,
    ExecutionTimeout,
)

from adapters.repository import AbstractNoSQLRepository


def verify_user(repo: AbstractNoSQLRepository, username: str, password: str) -> bool:
    res = repo.get_data(username=username)
    try:
        user = res.next()
    except StopIteration:  # wrong username
        return False

    if user["password"] == password:
        return True

    # wrong password
    return False


def retrieve_ip_data(repo: AbstractNoSQLRepository, ip: str) -> Dict[str, Any]:
    res = repo.get_data(ip=ip)

    try:
        data = res.next()
        return data
    except StopIteration:  # no result in database
        return {}


def save_ip_data(repo: AbstractNoSQLRepository, data: Dict[str, Any]) -> Tuple[Dict[str, str], int]:
    response = {"msg": ""}

    try:
        repo.save_data(data)
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


def delete_ip_data(repo: AbstractNoSQLRepository, ip: str) -> Tuple[Dict[str, str], int]:
    response = {"msg": ""}

    repo.delete_data(ip=ip)
    response["msg"] = "Deletion successful"
    return response, 200
