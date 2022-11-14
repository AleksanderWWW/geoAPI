import pytest

from dotenv import load_dotenv

from api import get_app
from adapters.repository import (
    MongoIPRepository,
    MongoUserRepository,
)

from geo_api_utils import get_mongo_collection

@pytest.fixture
def myapp():
    load_dotenv()
    
    user_repo = MongoUserRepository(
        get_mongo_collection("Sofomo", "users")
    )

    ip_repo = MongoIPRepository(
        get_mongo_collection("Sofomo", "geoAPI")
    )

    app = get_app(
        user_repo=user_repo,
        ip_repo=ip_repo
    )
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app


@pytest.fixture()
def client(myapp):
    return myapp.test_client()
