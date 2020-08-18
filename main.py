from flask import Flask, json, request
from recipeManagerDBC import RecipeManagerDBC
from model.RecipeSchema import RecipeSchema
from model.BookSchema import BookSchema

api = Flask(__name__)
dbc = RecipeManagerDBC()

recipe_schema = RecipeSchema()
book_schema = BookSchema()


@api.route("/recipes", methods=["GET"])
def get_recipes():
    return json.dumps(dbc.select_recipes()), 200


@api.route("/recipe/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    return json.dumps(dbc.select_recipe(recipe_id)), 200


@api.route("/recipe", methods=["POST"])
def add_recipe():
    errors = recipe_schema.validate(request.form)
    if errors:
        return json.dumps(errors), 400

    print(recipe_schema.validate(request.form))

    inserted_recipe_id = dbc.insert_recipe(request.form)

    # TODO: Add steps
    # TODO: Add tags

    return json.dumps({"message": "insertion successful", "inserted_recipe_id": inserted_recipe_id}), 201


@api.route("/recipe/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    return json.dumps({"message": f"deleted {dbc.delete_recipe(recipe_id)} row(s)"}), 200


@api.route("/books", methods=["GET"])
def get_books():
    return json.dumps(dbc.select_books()), 200


@api.route("/book/<int:book_id>", methods=["GET"])
def get_book(book_id):
    return json.dumps(dbc.select_book(book_id)), 200


@api.route("/book", methods=["POST"])
def add_book():
    errors = book_schema.validate(request.form)
    if errors:
        return json.dumps(errors), 400

    inserted_book_id = dbc.insert_book(request.form)

    # TODO: Add tags

    return json.dumps({"message": "insertion successful", "inserted_book_id": inserted_book_id}), 201


@api.route("/book/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    return json.dumps({"message": f"deleted {dbc.delete_book(book_id)} row(s)"}), 200


@api.route("/book/<int:book_id>/recipes", methods=["GET"])
def get_book_recipes(book_id):
    return json.dumps(dbc.select_recipes_from_book(book_id)), 200


@api.route("/book/<int:book_id>/recipe", methods=["POST"])
def add_recipe_to_book(book_id):
    dbc.insert_recipe_to_book(book_id, request.form.get("recipe_id"))
    return json.dumps({"message":  "insertion successful"}), 201


@api.route("/book/<int:book_id>/recipe/<int:recipe_id>", methods=["DELETE"])
def remove_recipe_from_book(book_id, recipe_id):
    return json.dumps({"message": f"deleted {dbc.delete_recipe_from_book(book_id, recipe_id)} row(s)"}), 200


if __name__ == "__main__":
    api.run()
