from flask import Blueprint, json, request
from marshmallow.validate import ValidationError

from src.DBC.recipeManagerDBC import RecipeManagerDBC
from src.DBC.authenticationDBC import AuthenticationDBC

from src.model.bookschema import InsertBookSchema, UpdateBookSchema
from src.model.bookrecipeschema import BookRecipeSchema


book_blueprint = Blueprint("book_endpoints", __name__)
dbc = RecipeManagerDBC.get_instance()
a_dbc = AuthenticationDBC.get_instance()

insert_book_schema = InsertBookSchema()
update_book_schema = UpdateBookSchema()

book_recipe_schema = BookRecipeSchema()


@book_blueprint.route("/books", methods=["GET"])
def get_books():
    return json.dumps(dbc.select_books()), 200


@book_blueprint.route("/book/<int:book_id>", methods=["GET"])
def get_book(book_id):
    if not dbc.recipe_exists(book_id):
        return json.dumps({"error": "Book not found"}), 404
    return json.dumps(dbc.select_book(book_id)), 200


@book_blueprint.route("/book", methods=["POST"])
def add_book():
    user_id, role = a_dbc.validate(request.cookies.get("session_id"))
    if role is None:
        return json.dumps({"message": "unauthorized"}), 401

    try:
        data = insert_book_schema.load(request.form)
    except ValidationError as e:
        return json.dumps(e.messages), 400

    inserted_book_id = dbc.insert_book(data)

    if "book_tags" in data:
        for tag_name in data["book_tags"]:
            dbc.insert_ignore_tag(tag_name)
            dbc.insert_tag_to_recipe(inserted_book_id, tag_name)

    return json.dumps({"message": "insertion successful", "book_id": inserted_book_id}), 201


@book_blueprint.route("/book/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    user_id, role = a_dbc.validate(request.cookies.get("session_id"))
    owner_id = dbc.book_exists(book_id)

    if owner_id is None:
        return json.dumps({"message": "Recipe not found"}), 404
    if not ((user_id == owner_id) or role == "admin"):
        return json.dumps({"message": "unauthorized"}), 401

    try:
        data = update_book_schema.load(request.form)
    except ValidationError as e:
        return json.dumps(e.messages), 400

    updated_row_count = dbc.update_book(book_id, request.form)

    if "book_tags" in data:
        dbc.delete_tags_from_book(book_id)
        for tag_name in data["book_tags"]:
            dbc.insert_ignore_tag(tag_name)
            dbc.insert_tag_to_book(book_id, tag_name)

    return json.dumps({"message": f"updated {updated_row_count} row(s)"}), 201


@book_blueprint.route("/book/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    user_id, role = a_dbc.validate(request.cookies.get("session_id"))
    owner_id = dbc.book_exists(book_id)

    if owner_id is None:
        return json.dumps({"message": "Recipe not found"}), 404
    if not ((user_id == owner_id) or role == "admin"):
        return json.dumps({"message": "unauthorized"}), 401

    return json.dumps({"message": f"deleted {dbc.delete_book(book_id)} row(s)"}), 200


@book_blueprint.route("/book/<int:book_id>/recipes", methods=["GET"])
def get_book_recipes(book_id):
    if not dbc.recipe_exists(book_id):
        return json.dumps({"error": "Book not found"}), 404

    return json.dumps(dbc.select_recipes_from_book(book_id)), 200


@book_blueprint.route("/book/<int:book_id>/recipe", methods=["POST"])
def add_recipe_to_book(book_id):
    user_id, role = a_dbc.validate(request.cookies.get("session_id"))
    owner_id = dbc.book_exists(book_id)

    print(user_id, role, owner_id)

    if owner_id is None:
        return json.dumps({"message": "Recipe not found"}), 404
    if not ((user_id == owner_id) or role == "admin"):
        return json.dumps({"message": "unauthorized"}), 401

    try:
        data = book_recipe_schema.load(request.form)
    except ValidationError as e:
        return json.dumps(e.messages), 400
    dbc.insert_recipe_to_book(book_id, data["recipe_id"])
    return json.dumps({"message":  "insertion successful"}), 201


@book_blueprint.route("/book/<int:book_id>/recipe/<int:recipe_id>", methods=["DELETE"])
def remove_recipe_from_book(book_id, recipe_id):
    user_id, role = a_dbc.validate(request.cookies.get("session_id"))
    owner_id = dbc.book_exists(book_id)

    if owner_id is None:
        return json.dumps({"message": "Recipe not found"}), 404
    if not ((user_id == owner_id) or role == "admin"):
        return json.dumps({"message": "unauthorized"}), 401
    
    return json.dumps({"message": f"deleted {dbc.delete_recipe_from_book(book_id, recipe_id)} row(s)"}), 200
