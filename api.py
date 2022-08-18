import os

from flask import Flask, jsonify, request

from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager
)

from dotenv import load_dotenv


# Dummy user data base
USERS = [
    {"username": "test",
    "password": "test-password"},
]


load_dotenv()


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["APP_SECRET_KEY"]

jwt = JWTManager(app)



@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username")
    password = request.json.get("password")

    for user in USERS:
        if user["username"] == username and user["password"] == password:
            access_token = create_access_token(username)
            return jsonify(access_token=access_token), 200

    resp_body = {
        "msg": "Bad username or password"
    }

    return jsonify(resp_body), 401


if __name__ == "__main__":
    app.run()