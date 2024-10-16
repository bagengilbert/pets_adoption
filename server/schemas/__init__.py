# server/schemas/__init__.py

from .user_schema import UserSchema
from .pet_schema import PetSchema
from .favorite_pet_schema import FavoritePetSchema
from .review_schema import ReviewSchema
from .shelter_schema import ShelterSchema
from .adoption_schema import AdoptionSchema

__all__ = [
    "UserSchema",
    "PetSchema",
    "FavoritePetSchema",
    "ReviewSchema",
    "ShelterSchema",
    "AdoptionSchema"
]
