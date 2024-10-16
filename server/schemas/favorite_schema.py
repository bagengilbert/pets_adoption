# server/schemas/favorite_schema.py

from marshmallow import Schema, fields, post_load
from server.models.favorite import Favorite

class FavoriteSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    pet_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_favorite(self, data, **kwargs):
        return Favorite(**data)
