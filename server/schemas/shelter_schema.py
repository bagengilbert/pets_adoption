# server/schemas/shelter_schema.py

from marshmallow import Schema, fields, validate, post_load
from server.models.shelter import Shelter

class ShelterSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    address = fields.Str(required=True, validate=validate.Length(min=1))
    contact_number = fields.Str(required=True, validate=validate.Length(min=10))
    website = fields.Url(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_shelter(self, data, **kwargs):
        return Shelter(**data)
