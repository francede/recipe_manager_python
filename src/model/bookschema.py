from marshmallow import Schema, fields, validates_schema
from marshmallow.validate import Length, ValidationError


class InsertBookSchema(Schema):
    book_name = fields.Str(required=True, validate=Length(min=1))
    book_tags = fields.List(fields.Int(), required=False)


class UpdateBookSchema(Schema):
    book_name = fields.Str(required=False, validate=Length(min=1))
    book_tags = fields.List(fields.Int(), required=False)

    @validates_schema()
    def validate_fields(self, data, **_):
        """Checks that at least one field is present"""
        if len(data) == 0:
            raise ValidationError("At least one field must be present to update.")
