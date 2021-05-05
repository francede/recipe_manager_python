from marshmallow import Schema, fields, validates_schema, pre_load
from marshmallow.validate import Length, ValidationError
from src.model.stepschema import StepSchema
from src.model.requestform_handler import form_data_to_dict
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
    def pre_load(self, form_data, **_):
        data = form_data_to_dict(form_data)

        if "recipe_tags" in data:
            data["recipe_tags"] = json.loads(data["recipe_tags"])
        if "recipe_steps" in data:
            data["recipe_steps"] = json.loads(data["recipe_steps"])
        return data


class UpdateRecipeSchema(Schema):
    recipe_name = fields.Str(required=False, validate=Length(min=1))
    recipe_active_time_minutes = fields.Int(required=False)
    recipe_total_time_minutes = fields.Int(required=False)
    recipe_description = fields.Str(required=False)
    recipe_servings = fields.Int(required=False)
    recipe_tags = fields.List(fields.Int(), required=False)
    recipe_steps = fields.List(fields.Nested(StepSchema), required=False)

    @validates_schema
    def validate_fields(self, data, **_):
        """Checks that at least one field is present"""
        if len(data) == 0:
            raise ValidationError("At least one field must be present to update.")

    @pre_load
    def pre_load(self, form_data, **_):
        data = form_data_to_dict(form_data)

        if "recipe_tags" in data:
            data["recipe_tags"] = json.loads(data["recipe_tags"])
        if "recipe_steps" in data:
            data["recipe_steps"] = json.loads(data["recipe_steps"])
        return data
