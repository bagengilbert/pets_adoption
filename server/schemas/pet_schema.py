# server/schemas/pet_schema.py

from marshmallow import Schema, fields, validate, post_load, validates, ValidationError
from server.models.pet import Pet

class PetSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    age = fields.Int(required=True, validate=validate.Range(min=0))
    species = fields.Str(required=True, validate=validate.Length(min=1))
    breed = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    image_url = fields.Url(required=True)
    user_id = fields.Int(dump_only=True)  # User ID who added the pet
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('age')
    def validate_age(self, age):
        if age < 0:
            raise ValidationError("Age must be a positive number.")

    @post_load
    def make_pet(self, data, **kwargs):
        return Pet(**data)
