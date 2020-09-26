from marshmallow import Schema, fields


class StepSchema(Schema):
    recipe_id = fields.Int(required=True)
    step_ordinal = fields.Int(required=True)
    step_instructions = fields.Str(required=True)
