from marshmallow import Schema, fields
from marshmallow.validate import Length


class RecipeSchema(Schema):
    recipe_name = fields.Str(required=True, validate=Length(min=1))
    recipe_active_time_minutes = fields.Int(required=False)
    recipe_total_time_minutes = fields.Int(required=False)
    recipe_description = fields.Str(required=False)
    recipe_servings = fields.Int(required=False)
