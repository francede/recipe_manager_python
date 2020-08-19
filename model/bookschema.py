from marshmallow import Schema, fields
from marshmallow.validate import Length


class BookSchema(Schema):
    book_name = fields.Str(required=True, validate=Length(min=1))
