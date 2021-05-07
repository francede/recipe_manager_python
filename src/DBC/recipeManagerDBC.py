import mysql.connector
import os

column_alias = {
    "recipe_name": "Name",
    "recipe_active_time_minutes": "ActiveTimeMinutes",
    "recipe_total_time_minutes": "TotalTimeMinutes",
    "recipe_description": "Description",
    "recipe_servings": "Servings",

    "book_name": "Name",
    "tag_name": "Name"
}


class RecipeManagerDBC:
    def __init__(self):
        host = os.environ.get("JAWSDB_MARIA_HOST", "localhost")
        database = os.environ.get("JAWSDB_MARIA_DATABASE", "recipemanager")
        user = os.environ.get("JAWSDB_MARIA_USER", "rm")
        password = os.environ.get("JAWSDB_MARIA_PASSWORD", "rmpassword")

        self.connection = mysql.connector.connect(host=host,
                                                  database=database,
                                                  user=user,
                                                  password=password)

    # RECIPES ---

    def select_recipes(self):
        c = self.connection.cursor(dictionary=True)
        c.execute("""SELECT
                             Recipes.RecipeID as recipe_id,
                             Recipes.Name as recipe_name,
                             Recipes.ActiveTimeMinutes as recipe_active_time_minutes,
                             Recipes.TotalTimeMinutes as recipe_total_time_minutes,
                             Recipes.Description as recipe_description,
                             Recipes.Servings as recipe_servings,
                             Users.Name as recipe_owner,
                             Users.UserID as recipe_owner_id
                             FROM Recipes INNER JOIN Users ON Recipes.UserID = Users.UserID""")
        recipes = c.fetchall()
        print(recipes)
        c.close()
        return recipes

    def select_recipe(self, recipe_id):
        c = self.connection.cursor(dictionary=True)
        c.execute("""SELECT
                     Recipes.RecipeID as recipe_id,
                     Recipes.Name as recipe_name,
                     Recipes.ActiveTimeMinutes as recipe_active_time_minutes,
                     Recipes.TotalTimeMinutes as recipe_total_time_minutes,
                     Recipes.Description as recipe_description,
                     Recipes.Servings as recipe_servings,
                     Users.Name as recipe_owner,
                     Users.UserID as recipe_owner_id
                     FROM Recipes INNER JOIN Users ON Recipes.UserID = Users.UserID
                     WHERE RecipeID = %s""",
                  (recipe_id,))
        recipe = c.fetchone()
        c.close()

        return recipe

    def insert_recipe(self, data, user_id):
        c = self.connection.cursor()
        c.execute("""
                  INSERT INTO Recipes (Name, ActiveTimeMinutes, TotalTimeMinutes, 
                  Description, Servings, UserID)
                  VALUES (%s, %s, %s, %s, %s, %s)
                  """,
                  (data["recipe_name"], data["recipe_active_time_minutes"],
                   data["recipe_total_time_minutes"], data["recipe_description"],
                   data["recipe_servings"], user_id))

        inserted_row_id = c.getlastrowid()

        self.connection.commit()
        c.close()
        return inserted_row_id

    def update_recipe(self, recipe_id, data):
        query = "UPDATE Recipes SET "
        c = self.connection.cursor()
        args = list()
        print(data)

        for key in data:
            query = query + f"{column_alias[key]} = %s, "
            args.append(data[key])

        # Slice comma and space after last "SET"
        query = query[:-2]

        query = query + " WHERE RecipeID = %s"
        args.append(recipe_id)

        c.execute(query, args)
        updated_row_count = c.rowcount

        self.connection.commit()
        c.close()

        return updated_row_count

    def delete_recipe(self, recipe_id):
        c = self.connection.cursor()
        c.execute("DELETE FROM Recipes WHERE RecipeID = %s", (recipe_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    def insert_tag_to_recipe(self, recipe_id, tag_id):
        c = self.connection.cursor()
        c.execute("INSERT INTO RecipeTags (RecipeID, TagID) VALUES (%s, %s)", (recipe_id, tag_id,))

        self.connection.commit()
        c.close()

    def delete_tags_from_recipe(self, recipe_id, tag_id=None):
        c = self.connection.cursor()

        if tag_id is None:
            c.execute("DELETE FROM RecipeTags WHERE RecipeID = %s", (recipe_id,))
        else:
            c.execute("DELETE FROM RecipeTags WHERE RecipeID = %s AND TagID = %s", (recipe_id, tag_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    # BOOKS ---

    def select_books(self):
        c = self.connection.cursor(dictionary=True)
        c.execute("SELECT * FROM Books")
        books = c.fetchall()
        c.close()
        return books

    def select_book(self, book_id):
        c = self.connection.cursor(dictionary=True)
        c.execute("SELECT * FROM Books WHERE BookID = %s",
                  (book_id,))
        book = c.fetchone()
        c.close()
        return book

    def insert_book(self, data):
        c = self.connection.cursor()
        c.execute("INSERT INTO Books (Name) VALUES (%s)",
                  (data["book_name"],))

        inserted_row_id = c.getlastrowid()
        self.connection.commit()
        c.close()
        return inserted_row_id

    def update_book(self, book_id, data):
        query = "UPDATE Books SET "
        c = self.connection.cursor()
        args = list()

        for key in data:
            query = query + f"{column_alias[key]} = %s, "
            args.append(data[key])

        # Slice comma and space after last "SET"
        query = query[:-2]

        query = query + " WHERE BookID = %s"
        args.append(book_id)

        c.execute(query, args)
        updated_row_count = c.rowcount

        self.connection.commit()
        c.close()

        return updated_row_count

    def delete_book(self, book_id):
        c = self.connection.cursor()
        c.execute("DELETE FROM Books WHERE BookID = %s", (book_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    def select_recipes_from_book(self, book_id):
        c = self.connection.cursor()
        c.execute("""
                  SELECT Recipes.RecipeID, Recipes.Name
                  FROM BookRecipes INNER JOIN Recipes
                  WHERE BookID = %s AND BookRecipes.RecipeID = Recipes.RecipeID
                  """, (book_id,))
        recipes = c.fetchall()
        c.close()
        return recipes

    def insert_recipe_to_book(self, book_id, recipe_id):
        c = self.connection.cursor()
        c.execute("INSERT INTO BookRecipes (BookID, RecipeID) VALUES (%s, %s)", (book_id, recipe_id,))

        self.connection.commit()
        c.close()

    def delete_recipe_from_book(self, book_id, recipe_id):
        c = self.connection.cursor()
        c.execute("DELETE FROM BookRecipes WHERE BookID = %s AND RecipeID = %s", (book_id, recipe_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    def insert_tag_to_book(self, book_id, tag_id):
        c = self.connection.cursor()
        c.execute("INSERT INTO BookTags (BookID, TagID) VALUES (%s, %s)", (book_id, tag_id,))

        self.connection.commit()
        c.close()

    def delete_tags_from_book(self, book_id, tag_id=None):
        c = self.connection.cursor()

        if tag_id is None:
            c.execute("DELETE FROM BookTags WHERE BookID = %s", (book_id,))
        else:
            c.execute("DELETE FROM BookTags WHERE BookID = %s AND TagID = %s", (book_id, tag_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    # TAGS ---

    def select_tags(self):
        c = self.connection.cursor(dictionary=True)
        c.execute("SELECT * FROM Tags")
        tags = c.fetchall()
        c.close()
        return tags

    def select_tags_by_recipe_id(self, recipe_id):
        c = self.connection.cursor()
        c.execute("""SELECT Tags.name FROM Recipes 
                             INNER JOIN RecipeTags ON Recipes.RecipeID = RecipeTags.RecipeID
                             INNER JOIN Tags ON RecipeTags.TagID = Tags.TagID
                             WHERE Recipes.RecipeID = %s
                             """,
                  (recipe_id,))

        tags = [t[0] for t in c.fetchall()]  # Flatten list
        c.close()
        return tags

    def insert_tag(self, data):
        c = self.connection.cursor()
        c.execute("INSERT INTO Tags (Name) VALUES (%s)", (data["tag_name"],))

        inserted_row_id = c.getlastrowid()

        self.connection.commit()
        c.close()
        return inserted_row_id

    def update_tag(self, tag_id, data):
        query = "UPDATE Tags SET "
        c = self.connection.cursor()
        args = list()

        for key in data:
            query = query + f"{column_alias[key]} = %s, "
            args.append(data[key])

        # Slice comma and space after last "SET"
        query = query[:-2]

        query = query + " WHERE TagID = %s"
        args.append(tag_id)

        c.execute(query, args)
        updated_row_count = c.rowcount

        self.connection.commit()
        c.close()

        return updated_row_count

    def delete_tag(self, tag_id):
        c = self.connection.cursor()
        c.execute("DELETE FROM Tags WHERE TagID = %s", (tag_id,))

        deleted_row_count = c.rowcount

        self.connection.commit()
        c.close()
        return deleted_row_count

    # STEPS ---

    def select_steps_by_recipe_id(self, recipe_id):
        c = self.connection.cursor()
        c.execute("""SELECT Steps.Instructions FROM Recipes 
                             INNER JOIN Steps ON Recipes.RecipeID = Steps.RecipeID
                             WHERE Recipes.RecipeID = %s
                             ORDER BY Steps.Ordinal ASC""",
                  (recipe_id,))

        steps = [s[0] for s in c.fetchall()]  # Flatten list
        c.close()
        return steps

    def insert_steps(self, recipe_id, recipe_steps):
        """
        :param recipe_id:
        :param recipe_steps: List of steps: {step_instructions:<str>}
        :return:
        """
        c = self.connection.cursor()
        q = "INSERT INTO Steps VALUES(%s, %s, %s)"
        d = [(recipe_id, i+1, recipe_steps[i]["step_instructions"]) for i in range(len(recipe_steps))]

        c.executemany(q, d)
        self.connection.commit()
        c.close()

    def delete_steps(self, recipe_id):
        c = self.connection.cursor()
        c.execute("DELETE FROM Steps WHERE RecipeID = %s", (recipe_id,) )

        self.connection.commit()
        c.close()
