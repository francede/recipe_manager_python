import mysql.connector
import os


class RecipeManagerDBC:
    def __init__(self):
        host = os.environ.get("JAWSDB_MARIA_HOST", "localhost")
        database = os.environ.get("JAWSDB_MARIA_DATABASE", "recipe_manager")
        user = os.environ.get("JAWSDB_MARIA_USER", "rm_user")
        password = os.environ.get("JAWSDB_MARIA_PASSWORD", "rmpassword")

        self.connection = mysql.connector.connect(host=host,
                                                  database=database,
                                                  user=user,
                                                  password=password)

    # RECIPES ---

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

    def insert_recipe(self, data):
        c = self.connection.cursor()
        c.execute("""
                  INSERT INTO recipe (recipe_name, recipe_active_time_minutes, recipe_total_time_minutes, 
                  recipe_description, recipe_servings)
                  VALUES (%s, %s, %s, %s, %s)
                  """,
                  (data["recipe_name"], data["recipe_active_time_minutes"],
                   data["recipe_total_time_minutes"], data["recipe_description"],
                   data["recipe_servings"]))

        inserted_row_id = c.getlastrowid()
        self.connection.commit()
        c.close()
        return inserted_row_id

    def update_recipe(self, recipe_id, data):
        query = "UPDATE recipe SET "
        c = self.connection.cursor()
        args = list()

        for key in data:
            query = query + f"{key} = %s, "
            args.append(data[key])

        # Slice comma and space after last "SET"
        query = query[:-2]

        query = query + " WHERE recipe_id = %s"
        args.append(recipe_id)

        c.execute(query, args)
        updated_row_count = c.rowcount

        self.connection.commit()
        c.close()

        return updated_row_count

    def delete_recipe(self, recipe_id):
        c = self.connection.cursor()
        c.execute("DELETE FROM recipe WHERE recipe_id = %s", (recipe_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    def insert_tag_to_recipe(self, recipe_id, tag_id):
        c = self.connection.cursor()
        c.execute("INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (%s, %s)", (recipe_id, tag_id,))

        self.connection.commit()
        c.close()

    def delete_tags_from_recipe(self, recipe_id, tag_id=None):
        c = self.connection.cursor()

        if tag_id is None:
            c.execute("DELETE FROM recipe_tags WHERE recipe_id = %s", (recipe_id,))
        else:
            c.execute("DELETE FROM recipe_tags WHERE recipe_id = %s AND tag_id = %s", (recipe_id, tag_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    # BOOKS ---

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

    def insert_book(self, data):
        c = self.connection.cursor()
        c.execute("INSERT INTO book (book_name) VALUES (%s)",
                  (data["book_name"],))

        inserted_row_id = c.getlastrowid()
        self.connection.commit()
        c.close()
        return inserted_row_id

    def update_book(self, book_id, data):
        query = "UPDATE book SET "
        c = self.connection.cursor()
        args = list()

        for key in data:
            query = query + f"{key} = %s, "
            args.append(data[key])

        # Slice comma and space after last "SET"
        query = query[:-2]

        query = query + " WHERE book_id = %s"
        args.append(book_id)

        c.execute(query, args)
        updated_row_count = c.rowcount

        self.connection.commit()
        c.close()

        return updated_row_count

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
                  SELECT recipe.recipe_id, recipe.recipe_name
                  FROM book_recipes INNER JOIN recipe
                  WHERE book_id = %s AND book_recipes.recipe_id = recipe.recipe_id
                  """, (book_id,))
        recipes = c.fetchall()
        c.close()
        return recipes

    def insert_recipe_to_book(self, book_id, recipe_id):
        c = self.connection.cursor()
        c.execute("INSERT INTO book_recipes (book_id, recipe_id) VALUES (%s, %s)", (book_id, recipe_id,))

        self.connection.commit()
        c.close()

    def delete_recipe_from_book(self, book_id, recipe_id):
        c = self.connection.cursor()
        c.execute("DELETE FROM book_recipes WHERE book_id = %s AND recipe_id = %s", (book_id, recipe_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    def insert_tag_to_book(self, book_id, tag_id):
        c = self.connection.cursor()
        c.execute("INSERT INTO book_tags (book_id, tag_id) VALUES (%s, %s)", (book_id, tag_id,))

        self.connection.commit()
        c.close()

    def delete_tags_from_book(self, book_id, tag_id=None):
        c = self.connection.cursor()

        if tag_id is None:
            c.execute("DELETE FROM book_tags WHERE book_id = %s", (book_id,))
        else:
            c.execute("DELETE FROM book_tags WHERE book_id = %s AND tag_id = %s", (book_id, tag_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    # TAGS ---

    def select_tags(self):
        c = self.connection.cursor()
        c.execute("SELECT * FROM tag")
        tags = c.fetchall()
        c.close()
        return tags

    def insert_tag(self, data):
        c = self.connection.cursor()
        c.execute("INSERT INTO tag (tag_name) VALUES (%s)", (data["tag_name"],))

        inserted_row_id = c.getlastrowid()

        self.connection.commit()
        c.close()
        return inserted_row_id

    def update_tag(self, tag_id, data):
        query = "UPDATE tag SET "
        c = self.connection.cursor()
        args = list()

        for key in data:
            query = query + f"{key} = %s, "
            args.append(data[key])

        # Slice comma and space after last "SET"
        query = query[:-2]

        query = query + " WHERE tag_id = %s"
        args.append(tag_id)

        c.execute(query, args)
        updated_row_count = c.rowcount

        self.connection.commit()
        c.close()

        return updated_row_count

    def delete_tag(self, tag_id):
        c = self.connection.cursor()
        c.execute("DELETE FROM tag WHERE tag_id = %s", (tag_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    # TODO: STEPS ---


