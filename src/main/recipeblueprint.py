from flask import Blueprint, json, request
from marshmallow.validate import ValidationError

from src.recipeManagerDBC import RecipeManagerDBC

from src.model.recipeschema import InsertRecipeSchema, UpdateRecipeSchema


recipe_blueprint = Blueprint("recipe_endpoints", __name__)
dbc = RecipeManagerDBC()

insert_recipe_schema = InsertRecipeSchema()
update_recipe_schema = UpdateRecipeSchema()


def form_data_to_dict(form_data):
    data = dict()
    for key in form_data:
        data[key] = form_data.get(key)
    return data


@recipe_blueprint.route("/recipes", methods=["GET"])
def get_recipes():
    return json.dumps(dbc.select_recipes()), 200


@recipe_blueprint.route("/recipe/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    return json.dumps(dbc.select_recipe(recipe_id)), 200


@recipe_blueprint.route("/recipe", methods=["POST"])
def add_recipe():
    try:
        data = insert_recipe_schema.load(form_data_to_dict(request.form))
    except ValidationError as e:
        return json.dumps(e.messages), 400

    inserted_recipe_id = dbc.insert_recipe(data)

    if "recipe_tags" in data:
        for tag_id in data["recipe_tags"]:
            dbc.insert_tag_to_recipe(inserted_recipe_id, tag_id)

    # TODO: Add steps

    return json.dumps({"message": "insertion successful", "recipe_id": inserted_recipe_id}), 201


@recipe_blueprint.route("/recipe/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    try:
        data = update_recipe_schema.load(form_data_to_dict(request.form))
    except ValidationError as e:
        return json.dumps(e.messages), 400

    updated_row_count = dbc.update_recipe(recipe_id, request.form)

    if "recipe_tags" in data:
        dbc.delete_tags_from_recipe(recipe_id)
        for tag_id in data["recipe_tags"]:
            dbc.insert_tag_to_recipe(recipe_id, tag_id)

    # TODO: Add steps

    return json.dumps({"message": f"updated {updated_row_count} row(s)"}), 201


@recipe_blueprint.route("/recipe/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    return json.dumps({"message": f"deleted {dbc.delete_recipe(recipe_id)} row(s)"}), 200

