from flask import Blueprint, json, request
from marshmallow.validate import ValidationError

from src.DBC.recipeManagerDBC import RecipeManagerDBC

from src.model.recipeschema import InsertRecipeSchema, UpdateRecipeSchema


recipe_blueprint = Blueprint("recipe_endpoints", __name__)
dbc = RecipeManagerDBC()

insert_recipe_schema = InsertRecipeSchema()
update_recipe_schema = UpdateRecipeSchema()


@recipe_blueprint.route("/recipes", methods=["GET"])
def get_recipes():
    return json.dumps(dbc.select_recipes()), 200


@recipe_blueprint.route("/recipe/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = dbc.select_recipe(recipe_id)
    if recipe is None:
        return json.dumps({"error": "Recipe not found"}), 404
    recipe["recipe_tags"] = dbc.select_tags_by_recipe_id(recipe_id)
    recipe["recipe_steps"] = dbc.select_steps_by_recipe_id(recipe_id)
    return json.dumps(recipe), 200


@recipe_blueprint.route("/recipe", methods=["POST"])
def add_recipe():
    try:
        data = insert_recipe_schema.load(request.form)
    except ValidationError as e:
        return json.dumps(e.messages), 400

    inserted_recipe_id = dbc.insert_recipe(data, 1)

    if "recipe_tags" in data:
        for tag_id in data["recipe_tags"]:
            dbc.insert_tag_to_recipe(inserted_recipe_id, tag_id)

    if "recipe_steps" in data:
        dbc.insert_steps(inserted_recipe_id, data["recipe_steps"])

    return json.dumps({"message": "insertion successful", "recipe_id": inserted_recipe_id}), 201


@recipe_blueprint.route("/recipe/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    if not dbc.recipe_exists(recipe_id):
        return json.dumps({"error": "Recipe not found"}), 404

    try:
        data = update_recipe_schema.load(request.form)
    except ValidationError as e:
        return json.dumps(e.messages), 400

    tags = data.pop("recipe_tags", None)
    steps = data.pop("recipe_steps", None)

    updated_row_count = dbc.update_recipe(recipe_id, data)

    if tags is not None:
        dbc.delete_tags_from_recipe(recipe_id)
        for tag_id in tags:
            dbc.insert_tag_to_recipe(recipe_id, tag_id)

    if steps is not None:
        dbc.delete_steps(recipe_id)
        dbc.insert_steps(recipe_id, steps)

    return json.dumps({"message": f"updated {updated_row_count} row(s)"}), 201


@recipe_blueprint.route("/recipe/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    if not dbc.recipe_exists(recipe_id):
        return json.dumps({"error": "Recipe not found"}), 404

    return json.dumps({"message": f"deleted {dbc.delete_recipe(recipe_id)} row(s)"}), 200

