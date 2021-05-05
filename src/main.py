from flask import Flask
from src.DBC.recipeManagerDBC import RecipeManagerDBC

from src.main.recipeblueprint import recipe_blueprint
from src.main.bookblueprint import book_blueprint
from src.main.tagblueprint import tag_blueprint


app = Flask(__name__)
app.register_blueprint(recipe_blueprint)
app.register_blueprint(book_blueprint)
app.register_blueprint(tag_blueprint)

#dbc = RecipeManagerDBC()

if __name__ == "__main__":
    app.run()
