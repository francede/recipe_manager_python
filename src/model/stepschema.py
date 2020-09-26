from marshmallow import Schema, fields


class StepSchema(Schema):
    # recipe_id = fields.Int(required=True) # Not needed as steps are currently passed only with the recipe itself
    # step_ordinal = fields.Int(required=True) # Not needed yet as all steps are passed for update
    step_instructions = fields.Str(required=True)
