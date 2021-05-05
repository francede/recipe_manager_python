from flask import Blueprint, json, request
from marshmallow.validate import ValidationError

from src.DBC.recipeManagerDBC import RecipeManagerDBC

from src.model.tagschema import InsertTagSchema, UpdateTagSchema


tag_blueprint = Blueprint("tag_endpoints", __name__)
dbc = RecipeManagerDBC()

insert_tag_schema = InsertTagSchema()
update_tag_schema = UpdateTagSchema()


@tag_blueprint.route("/tags", methods=["GET"])
def get_tags():
    return json.dumps(dbc.select_tags()), 200


@tag_blueprint.route("/tag", methods=["POST"])
def add_tag():
    try:
        data = insert_tag_schema.load(request.form)
    except ValidationError as e:
        return json.dumps(e.messages), 400

    inserted_tag_id = dbc.insert_tag(data)

    return json.dumps({"message": "insertion successful", "tag_id": inserted_tag_id}), 201


@tag_blueprint.route("/tag/<int:tag_id>", methods=["PUT"])
def update_tag(tag_id):
    try:
        data = update_tag_schema.load(request.form)
    except ValidationError as e:
        return json.dumps(e.messages), 400

    updated_row_count = dbc.update_tag(tag_id, data)

    return json.dumps({"message": f"updated {updated_row_count} row(s)"}), 201


@tag_blueprint.route("/tag/<int:tag_id>", methods=["DELETE"])
def delete_tag(tag_id):
    return json.dumps({"message": f"deleted {dbc.delete_tag(tag_id)} row(s)"}), 200
