# server/schemas/review_schema.py

from marshmallow import Schema, fields, validate, post_load
from server.models.review import Review

class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    pet_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_review(self, data, **kwargs):
        return Review(**data)
