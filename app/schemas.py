from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    user_id = fields.Int(required=True)
    user = fields.Nested(UserSchema, dump_only=True)

class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    create_date = fields.DateTime(dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)
    category = fields.Nested(CategorySchema, dump_only=True)

