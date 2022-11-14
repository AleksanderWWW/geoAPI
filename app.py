import os

from dotenv import load_dotenv

from adapters.repository import (
    MongoIPRepository,
    MongoUserRepository,
)
from api import get_app
from geo_api_utils import get_mongo_collection


def main():
    load_dotenv()

    user_repo = MongoUserRepository(get_mongo_collection(os.environ["MONGO_CONN_STR"], "Sofomo", "users"))

    ip_repo = MongoIPRepository(get_mongo_collection(os.environ["MONGO_CONN_STR"], "Sofomo", "geoAPI"))

    app = get_app(user_repo=user_repo, ip_repo=ip_repo)

    app.run(debug=True)


if __name__ == "__main__":
    main()
