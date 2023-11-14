from marshmallow import fields, Schema, validate

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=250))

class FoodSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=250))
    description = fields.Str()
    picture = fields.Str()
    ingredients = fields.Str()
    category = fields.Nested(CategorySchema) 