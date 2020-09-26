from flask import Flask, json, request
from src.recipeManagerDBC import RecipeManagerDBC
from src.model.recipeschema import InsertRecipeSchema, UpdateRecipeSchema
from src.model.bookschema import InsertBookSchema, UpdateBookSchema
from src.model.tagschema import InsertTagSchema, UpdateTagSchema

api = Flask(__name__)
dbc = RecipeManagerDBC()

insert_recipe_schema = InsertRecipeSchema()
update_recipe_schema = UpdateRecipeSchema()
insert_book_schema = InsertBookSchema()
update_book_schema = UpdateBookSchema()
insert_tag_schema = InsertTagSchema()
update_tag_schema = UpdateTagSchema()


@api.route("/recipes", methods=["GET"])
def get_recipes():
    return json.dumps(dbc.select_recipes()), 200


@api.route("/recipe/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    return json.dumps(dbc.select_recipe(recipe_id)), 200


@api.route("/recipe", methods=["POST"])
def add_recipe():
    errors = insert_recipe_schema.validate(request.form)
    if errors:
        return json.dumps(errors), 400

    inserted_recipe_id = dbc.insert_recipe(request.form)

    if request.form["recipe_tags"]:
        for tag_id in request.form["recipe_tags"]:
            dbc.insert_tag_to_recipe(inserted_recipe_id, tag_id)

    # TODO: Add steps

    return json.dumps({"message": "insertion successful", "recipe_id": inserted_recipe_id}), 201


@api.route("/recipe/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    errors = update_recipe_schema.validate(request.form)
    if errors:
        return json.dumps(errors), 400

    updated_row_count = dbc.update_recipe(recipe_id, request.form)

    if request.form["recipe_tags"]:
        dbc.delete_tag_from_recipe(recipe_id)
        for tag_id in request.form["recipe_tags"]:
            dbc.insert_tag_to_recipe(recipe_id, tag_id)

    # TODO: Add steps

    return json.dumps({"message": f"updated {updated_row_count} row(s)"}), 201


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
    errors = insert_book_schema.validate(request.form)
    if errors:
        return json.dumps(errors), 400

    inserted_book_id = dbc.insert_book(request.form)

    if request.form["book_tags"]:
        for tag_id in request.form["recipe_tags"]:
            dbc.insert_tag_to_recipe(inserted_book_id, tag_id)

    return json.dumps({"message": "insertion successful", "book_id": inserted_book_id}), 201


@api.route("/book/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    errors = update_book_schema.validate(request.form)
    if len(request.form) == 0:
        errors["form"] = ["No fields given to update."]
    if errors:
        return json.dumps(errors), 400

    updated_row_count = dbc.update_book(book_id, request.form)

    if request.form["book_tags"]:
        dbc.delete_tag_from_recipe(book_id)
        for tag_id in request.form["book_tags"]:
            dbc.insert_tag_to_recipe(book_id, tag_id)

    return json.dumps({"message": f"updated {updated_row_count} row(s)"}), 201


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


@api.route("/tags", methods=["GET"])
def get_tags():
    return json.dumps(dbc.select_tags()), 200


@api.route("/tag", methods=["POST"])
def add_tag():
    errors = insert_tag_schema.validate(request.form)
    if errors:
        return json.dumps(errors), 400

    inserted_tag_id = dbc.insert_tag(request.form)

    return json.dumps({"message": "insertion successful", "tag_id": inserted_tag_id}), 201


@api.route("/tag/<int:tag_id>", methods=["PUT"])
def update_tag(tag_id):
    errors = update_tag_schema.validate(request.form)
    if len(request.form) == 0:
        errors["form"] = ["No fields given to update."]
    if errors:
        return json.dumps(errors), 400

    updated_row_count = dbc.update_tag(tag_id, request.form)

    return json.dumps({"message": f"updated {updated_row_count} row(s)"}), 201


@api.route("/tag/<int:tag_id>", methods=["DELETE"])
def delete_tag(tag_id):
    return json.dumps({"message": f"deleted {dbc.delete_tag(tag_id)} row(s)"}), 200


if __name__ == "__main__":
    api.run()
