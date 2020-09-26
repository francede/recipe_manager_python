from marshmallow import Schema, fields, validates_schema
from marshmallow.validate import Length, ValidationError


class InsertRecipeSchema(Schema):
    recipe_name = fields.Str(required=True, validate=Length(min=1))
    recipe_active_time_minutes = fields.Int(required=False)
    recipe_total_time_minutes = fields.Int(required=False)
    recipe_description = fields.Str(required=False)
    recipe_servings = fields.Int(required=False)
    recipe_tags = fields.List(fields.Int(), required=False)


class UpdateRecipeSchema(Schema):
    recipe_name = fields.Str(required=False, validate=Length(min=1))
    recipe_active_time_minutes = fields.Int(required=False)
    recipe_total_time_minutes = fields.Int(required=False)
    recipe_description = fields.Str(required=False)
    recipe_servings = fields.Int(required=False)
    recipe_tags = fields.List(fields.Int(), required=False)

    @validates_schema()
    def validate_fields(self, data, **_):
        """Checks that at least one field is present"""
        if len(data) == 0:
            raise ValidationError("At least one field must be present to update.")
