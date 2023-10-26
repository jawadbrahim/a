from marshmallow import Schema, fields, validate


class JuiceSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=250))
    description = fields.Str()
    ingredients=fields.Str()
    picture=fields.Str()
