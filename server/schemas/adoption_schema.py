# server/schemas/adoption_schema.py

from marshmallow import Schema, fields, validate, post_load, ValidationError
from server.models.adoption import Adoption

class AdoptionSchema(Schema):
    id = fields.Int(dump_only=True)
    pet_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(["pending", "approved", "rejected"]))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_adoption(self, data, **kwargs):
        return Adoption(**data)
