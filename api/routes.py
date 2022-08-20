import os

from datetime import timedelta

from flask import Flask, jsonify, request

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    JWTManager
)

from dotenv import load_dotenv

from utils import parse_request, fetch_ip_data, get_mongo_collection, save_ip_data, verify_user


load_dotenv()


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["APP_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

# for IP STACK access
ip_stack_key = os.environ["IP_STACK_KEY"]
geo_api_collection = get_mongo_collection(os.environ["MONGO_CONN_STR"], "Sofomo", "geoAPI")
users_collection = get_mongo_collection(os.environ["MONGO_CONN_STR"], "Sofomo", "users")



@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username")
    password = request.json.get("password")

    verification_flag = verify_user(username, password, users_collection)
    if verification_flag:
        access_token = create_access_token(username)
        return jsonify(access_token=access_token), 200
    
    resp_body = {
        "msg": "Bad username or password"
    }

    return jsonify(resp_body), 401


@app.route("/status")
def status():
    return jsonify({"status": "ok"}), 200


@app.route("/api/add", methods=["POST"])
@jwt_required()
def add_geo_data():
    # parse request for ip address
    ip = parse_request(request)

    if not ip:
        return jsonify({"msg": "No IP address supplied"}), 400

    data = fetch_ip_data(ip, ip_stack_key)

    
    resp, code = save_ip_data(data, geo_api_collection)
    print(data)

    return jsonify(resp), code


@app.route("/api/retrieve", methods=["GET"])
@jwt_required()
def get_geo_data():
    ip = parse_request(request)

    if not ip:
        return jsonify({"msg": "No IP address supplied"}), 400

    data = fetch_ip_data(ip, ip_stack_key)

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
