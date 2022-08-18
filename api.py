from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/token", methods=["POST"])
def create_token():
    resp_body = {"hello": "world"}
    return jsonify(resp_body)


if __name__ == "__main__":
    app.run()