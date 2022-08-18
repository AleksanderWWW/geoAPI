import os

from flask import Flask, jsonify

from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["APP_SECRET_KEY"]


@app.route("/token", methods=["POST"])
def create_token():
    resp_body = {"hello": "world"}
    return jsonify(resp_body)


if __name__ == "__main__":
    app.run()