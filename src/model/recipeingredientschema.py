from marshmallow import Schema, fields


class RecipeIngredientSchema(Schema):
    recipe_id = fields.Int(required=True)
    ingredient_id = fields.Int(required=True)
    recipe_ingredient_amount = fields.Float(required=True)
    recipe_ingredient_unit = fields.Str(required=False)
