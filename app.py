import os
from datetime import timedelta

from dotenv import load_dotenv

from api import app
from api.utils import get_mongo_collection

load_dotenv()

app.config["SECRET_KEY"] = os.environ["APP_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["IP_STACK_KEY"] = os.environ["IP_STACK_KEY"]
app.config["GEO_API_COLLECTION"] = get_mongo_collection(os.environ["MONGO_CONN_STR"], "Sofomo", "geoAPI")
app.config["USERS_COLLECTION"] = get_mongo_collection(os.environ["MONGO_CONN_STR"], "Sofomo", "users")


if __name__ == "__main__":
    app.run(debug=True)
