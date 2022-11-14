import os

from flask import (
    Flask,
    jsonify,
    request,
)

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
)

from adapters.repository import AbstractNoSQLRepository

from services.model import (
    delete_ip_data,
    retrieve_ip_data,
    save_ip_data,
    verify_user,
)

from api.backend import (
    fetch_ip_data,
    parse_request,
)

from api.constants import JWT_TOKEN_EXPIRY_TIME_INTERVAL


def get_app(
    ip_repo: AbstractNoSQLRepository,
    user_repo: AbstractNoSQLRepository,
) -> Flask:

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ["APP_SECRET_KEY"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_TOKEN_EXPIRY_TIME_INTERVAL
    app.config["IP_STACK_KEY"] = os.environ["IP_STACK_KEY"]

    jwt = JWTManager(app)


    @app.route("/token", methods=["POST"])
    def create_token():
        username = request.json.get("username")
        password = request.json.get("password")

        verification_flag = verify_user(user_repo, username, password)
        if verification_flag:
            access_token = create_access_token(username)
            return jsonify(access_token=access_token), 200

        resp_body = {"msg": "Bad username or password"}

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

        resp, code = save_ip_data(ip_repo, data)

        return jsonify(resp), code


    @app.route("/api/retrieve", methods=["GET"])
    @jwt_required()
    def get_geo_data():
        ip = parse_request(request)

        if not ip:
            return jsonify({"msg": "No IP address supplied"}), 400

        data = retrieve_ip_data(ip_repo, ip)

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

        resp, code = delete_ip_data(ip_repo, ip)
        return jsonify(resp), code

    return app
