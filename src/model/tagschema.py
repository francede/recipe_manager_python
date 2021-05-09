from marshmallow import Schema, fields, validates_schema
from marshmallow.validate import Length, ValidationError


class InsertTagSchema(Schema):
    tag_name = fields.Str(required=True, validate=Length(min=1))


"""
class UpdateTagSchema(Schema):
    tag_name = fields.Str(required=False, validate=Length(min=1))

    @validates_schema()
    def validate_fields(self, data, **_):
        ""Checks that at least one field is present""
        if len(data) == 0:
            raise ValidationError("At least one field must be present to update.")
"""