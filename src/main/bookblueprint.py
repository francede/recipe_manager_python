from flask import Blueprint, json, request
from marshmallow.validate import ValidationError

from src.recipeManagerDBC import RecipeManagerDBC

from src.model.bookschema import InsertBookSchema, UpdateBookSchema
from src.model.bookrecipeschema import BookRecipeSchema


book_blueprint = Blueprint("book_endpoints", __name__)
dbc = RecipeManagerDBC()

insert_book_schema = InsertBookSchema()
update_book_schema = UpdateBookSchema()

book_recipe_schema = BookRecipeSchema()


def form_data_to_dict(form_data):
    data = dict()
    for key in form_data:
        data[key] = form_data.get(key)
    return data


@book_blueprint.route("/books", methods=["GET"])
def get_books():
    return json.dumps(dbc.select_books()), 200


@book_blueprint.route("/book/<int:book_id>", methods=["GET"])
def get_book(book_id):
    return json.dumps(dbc.select_book(book_id)), 200


@book_blueprint.route("/book", methods=["POST"])
def add_book():
    try:
        data = insert_book_schema.load(form_data_to_dict(request.form))
    except ValidationError as e:
        return json.dumps(e.messages), 400

    inserted_book_id = dbc.insert_book(data)

    if "book_tags" in data:
        for tag_id in data["recipe_tags"]:
            dbc.insert_tag_to_recipe(inserted_book_id, tag_id)

    return json.dumps({"message": "insertion successful", "book_id": inserted_book_id}), 201


@book_blueprint.route("/book/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    try:
        data = update_book_schema.load(form_data_to_dict(request.form))
    except ValidationError as e:
        return json.dumps(e.messages), 400

    updated_row_count = dbc.update_book(book_id, request.form)

    if "book_tags" in data:
        dbc.delete_tags_from_book(book_id)
        for tag_id in data["book_tags"]:
            dbc.insert_tag_to_book(book_id, tag_id)

    return json.dumps({"message": f"updated {updated_row_count} row(s)"}), 201


@book_blueprint.route("/book/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    return json.dumps({"message": f"deleted {dbc.delete_book(book_id)} row(s)"}), 200


@book_blueprint.route("/book/<int:book_id>/recipes", methods=["GET"])
def get_book_recipes(book_id):
    return json.dumps(dbc.select_recipes_from_book(book_id)), 200


@book_blueprint.route("/book/<int:book_id>/recipe", methods=["POST"])
def add_recipe_to_book(book_id):
    try:
        data = book_recipe_schema.load(form_data_to_dict(request.form))
    except ValidationError as e:
        return json.dumps(e.messages), 400
    dbc.insert_recipe_to_book(book_id, data["recipe_id"])
    return json.dumps({"message":  "insertion successful"}), 201


@book_blueprint.route("/book/<int:book_id>/recipe/<int:recipe_id>", methods=["DELETE"])
def remove_recipe_from_book(book_id, recipe_id):
    return json.dumps({"message": f"deleted {dbc.delete_recipe_from_book(book_id, recipe_id)} row(s)"}), 200
