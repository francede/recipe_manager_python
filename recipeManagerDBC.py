import mysql.connector
from model.RecipeSchema import RecipeSchema
from model.BookSchema import BookSchema


class RecipeManagerDBC:
    def __init__(self):
        self.connection = mysql.connector.connect(host="localhost",
                                                  database="recipe_manager",
                                                  user="rm_user",
                                                  password="rmpassword")

    def select_recipes(self):
        c = self.connection.cursor()
        c.execute("SELECT * FROM recipe")
        recipes = c.fetchall()
        c.close()
        return recipes

    def select_recipe(self, recipe_id):
        c = self.connection.cursor()
        c.execute("SELECT * FROM recipe WHERE recipe_id = %s",
                  (recipe_id,))
        recipe = c.fetchone()
        c.close()
        return recipe

    def insert_recipe(self, form_data):
        c = self.connection.cursor()
        c.execute("""
                  INSERT INTO recipe (name, active_time_minutes, total_time_minutes, description, servings)
                  VALUES (%s, %s, %s, %s, %s)
                  """,
                  (form_data.get("recipe_name"), form_data.get("recipe_active_time_minutes"),
                   form_data.get("recipe_total_time_minutes"), form_data.get("recipe_description"),
                   form_data.get("recipe_servings")))

        inserted_row_id = c.getlastrowid()
        self.connection.commit()
        c.close()
        return inserted_row_id

    def update_recipe(self, recipe):
        pass

    def delete_recipe(self, recipe_id):
        c = self.connection.cursor()
        c.execute("DELETE FROM recipe WHERE recipe_id = %s", (recipe_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    def select_books(self):
        c = self.connection.cursor()
        c.execute("SELECT * FROM book")
        books = c.fetchall()
        c.close()
        return books

    def select_book(self, book_id):
        c = self.connection.cursor()
        c.execute("SELECT * FROM book WHERE book_id = %s",
                  (book_id,))
        book = c.fetchone()
        c.close()
        return book

    def insert_book(self, form_data):
        c = self.connection.cursor()
        c.execute("INSERT INTO book (name) VALUES (%s)",
                  (form_data.get("book_name"),))

        inserted_row_id = c.getlastrowid()
        self.connection.commit()
        c.close()
        return inserted_row_id

    def delete_book(self, book_id):
        c = self.connection.cursor()
        c.execute("DELETE FROM book WHERE book_id = %s", (book_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    def select_recipes_from_book(self, book_id):
        c = self.connection.cursor()
        c.execute("""
                  SELECT recipe.recipe_id, recipe.name
                  FROM book_recipes INNER JOIN recipe
                  WHERE book_id = %s AND book_recipes.recipe_id = recipe.recipe_id
                  """, (book_id,))
        recipes = c.fetchall()
        c.close()
        return recipes

    def insert_recipe_to_book(self, book_id, recipe_id):
        c = self.connection.cursor()
        c.execute("INSERT INTO book_recipes (book_id, recipe_id) VALUES (%s, %s)", (book_id, recipe_id,))

        print(c.getlastrowid())
        self.connection.commit()
        c.close()

    def delete_recipe_from_book(self, book_id, recipe_id):
        c = self.connection.cursor()
        c.execute("DELETE FROM book_recipes WHERE book_id = %s AND recipe_id = %s", (book_id, recipe_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count
