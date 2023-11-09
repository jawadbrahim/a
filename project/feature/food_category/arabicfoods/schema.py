from marshmallow import Schema, fields, validate

class ArabicfoodSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=250))
    description = fields.Str()
    picture = fields.Str()
    ingredients=fields.Str()