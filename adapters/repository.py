from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Dict,
)

from pymongo.collection import Collection


class AbstractNoSQLRepository(ABC):
    @abstractmethod
    def get_data(self, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def save_data(self, data: Dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_data(self, **kwargs) -> None:
        raise NotImplementedError


class MongoIPRepository(AbstractNoSQLRepository):
    def __init__(self, collection: Collection) -> None:

        super().__init__()

        self._collection = collection

    def get_data(self, **kwargs) -> Dict[str, Any]:
        ip = kwargs["ip"]
        return self._collection.find({"ip": ip})

    def save_data(self, data: Dict) -> None:
        ip = data["ip"]

        if self._collection.count_documents({"ip": ip}):
            return

        self._collection.insert_one(data)

    def delete_data(self, **kwargs) -> None:
        ip = kwargs["ip"]
        self._collection.delete_one({"ip": ip})


class MongoUserRepository(AbstractNoSQLRepository):
    def __init__(self, collection: Collection) -> None:

        super().__init__()

        self._collection = collection

    def get_data(self, **kwargs) -> Dict[str, Any]:
        user_name = kwargs["username"]
        return self._collection.find({"username": user_name})

    def save_data(self, data: Dict) -> None:
        ...

    def delete_data(self, **kwargs) -> None:
        ...
