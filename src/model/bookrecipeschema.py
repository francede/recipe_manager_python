from marshmallow import Schema, fields


class BookRecipeSchema(Schema):
    recipe_id = fields.Int(required=True)
