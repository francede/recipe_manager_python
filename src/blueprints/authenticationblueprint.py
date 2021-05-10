from flask import Blueprint, json, request, make_response
import hashlib

from src.DBC.authenticationDBC import AuthenticationDBC


authentication_blueprint = Blueprint("authentication_endpoints", __name__)
a_dbc = AuthenticationDBC()


@authentication_blueprint.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    new_role = request.form.get("role")
    h = hashlib.sha256()
    h.update(password.encode("utf-8"))
    password_hash = h.hexdigest()

    user_id, role = a_dbc.validate(request.cookies.get("session_id"))

    if role != "admin":
        return json.dumps({"message": "only admins are authorized to register users"}), 401

    success, msg = a_dbc.register(username, password_hash, new_role)
    if not success:
        json.dumps({"message": msg}), 400

    return json.dumps({"message": username + " registered as " + new_role}), 200


@authentication_blueprint.route("/login", methods=["POST"])
def login():
    username, password = a_dbc.parse_basic_auth(request.headers["Authorization"])
    h = hashlib.sha256()
    h.update(password.encode("utf-8"))
    password_hash = h.hexdigest()
    session_id = a_dbc.login(username, password_hash)
    response = make_response(json.dumps({"message": "Logged in as " + username}))
    response.set_cookie("session_id", session_id, httponly=True)
    response.set_cookie("current_user", username)
    return response, 200
