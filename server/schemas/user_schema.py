# server/schemas/user_schema.py

from marshmallow import Schema, fields, validate, post_load, pre_load, ValidationError
from server.models.user import User
from werkzeug.security import generate_password_hash

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @pre_load
    def hash_password(self, data, **kwargs):
        if "password" in data:
            data["password"] = generate_password_hash(data["password"])
        return data

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
