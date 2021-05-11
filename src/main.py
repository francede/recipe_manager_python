from flask import Flask

from src.blueprints.recipeblueprint import recipe_blueprint
from src.blueprints.bookblueprint import book_blueprint
from src.blueprints.tagblueprint import tag_blueprint
from src.blueprints.authenticationblueprint import authentication_blueprint


app = Flask(__name__)
app.register_blueprint(recipe_blueprint, url_prefix="/api")
app.register_blueprint(book_blueprint, url_prefix="/api")
app.register_blueprint(tag_blueprint, url_prefix="/api")
app.register_blueprint(authentication_blueprint, url_prefix="/api")


@app.after_request
def cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run()
