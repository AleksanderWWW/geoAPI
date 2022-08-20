from flask import Flask, jsonify, request

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    JWTManager
)

from api.utils import (
    verify_user,
    parse_request, 
    fetch_ip_data, 
    save_ip_data,
    retrieve_ip_data,
    delete_ip_data 
    )


app = Flask(__name__)

jwt = JWTManager(app)


@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username")
    password = request.json.get("password")

    verification_flag = verify_user(username, password, app.config["USERS_COLLECTION"])
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

    data = fetch_ip_data(ip, app.config["IP_STACK_KEY"])

    
    resp, code = save_ip_data(data, app.config["GEO_API_COLLECTION"])

    return jsonify(resp), code


@app.route("/api/retrieve", methods=["GET"])
@jwt_required()
def get_geo_data():
    ip = parse_request(request)

    if not ip:
        return jsonify({"msg": "No IP address supplied"}), 400

    data = retrieve_ip_data(ip, app.config["GEO_API_COLLECTION"])

    if data:
        code = 200
    
    else:
        code = 404

    return jsonify(data), code


@app.route("/api/delete", methods=["DELETE"])
@jwt_required()
def delete_geo_data():
    ip = parse_request(request)

    if not ip:
        return jsonify({"msg": "No IP address supplied"}), 400

    resp, code = delete_ip_data(ip, app.config["GEO_API_COLLECTION"])
    return jsonify(resp), code
