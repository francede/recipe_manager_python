from marshmallow import Schema, fields, validates_schema, pre_load
from marshmallow.validate import Length, ValidationError
from src.model.stepschema import StepSchema
import json


class InsertRecipeSchema(Schema):
    recipe_name = fields.Str(required=True, validate=Length(min=1))
    recipe_active_time_minutes = fields.Int(required=False)
    recipe_total_time_minutes = fields.Int(required=False)
    recipe_description = fields.Str(required=False)
    recipe_servings = fields.Int(required=False)
    recipe_tags = fields.List(fields.Int(), required=False)
    recipe_steps = fields.List(fields.Nested(StepSchema), required=False)

    @pre_load
    def pre_load(self, data, **_):
        print(data)
        print(type(data["recipe_steps"]))
        if "recipe_tags" in data:
            data["recipe_tags"] = json.loads(data["recipe_tags"])
        if "recipe_steps" in data:
            data["recipe_steps"] = json.loads(data["recipe_steps"])
        print("PRE_LOAD")
        print(data)
        return data


class UpdateRecipeSchema(Schema):
    recipe_name = fields.Str(required=False, validate=Length(min=1))
    recipe_active_time_minutes = fields.Int(required=False)
    recipe_total_time_minutes = fields.Int(required=False)
    recipe_description = fields.Str(required=False)
    recipe_servings = fields.Int(required=False)
    recipe_tags = fields.List(fields.Int(), required=False)

    @validates_schema
    def validate_fields(self, data, **_):
        """Checks that at least one field is present"""
        if len(data) == 0:
            raise ValidationError("At least one field must be present to update.")
