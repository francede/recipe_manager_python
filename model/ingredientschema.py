from marshmallow import Schema, fields
from marshmallow.validate import Length


class IngredientSchema(Schema):
    ingredient_name = fields.Str(required=True, validate=Length(min=1))
