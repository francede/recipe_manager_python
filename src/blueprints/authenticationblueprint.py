from flask import Blueprint, json

from src.DBC.recipeManagerDBC import RecipeManagerDBC


authentication_blueprint = Blueprint("authentication_endpoints", __name__)
dbc = RecipeManagerDBC()


@authentication_blueprint.route("/register", methods=["POST"])
def register_user():
    return json.dumps({"message": "Not yet implemented"}), 200


@authentication_blueprint.route("/login", methods=["POST"])
def login():
    return json.dumps({"message": "Not yet implemented"}), 200


@authentication_blueprint.route("/user", methods=["DELETE"])
def register_user():
    return json.dumps({"message": "Not yet implemented"}), 200
