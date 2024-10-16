# server/schemas/__init__.py

from .user_schema import UserSchema
from .pet_schema import PetSchema
from .favorite_schema import FavoriteSchema  # Importing the FavoriteSchema
from .review_schema import ReviewSchema
from .shelter_schema import ShelterSchema
from .adoption_schema import AdoptionSchema

__all__ = [
    "UserSchema",
    "PetSchema",
    "FavoriteSchema",  # Include the FavoriteSchema in the exports
    "ReviewSchema",
    "ShelterSchema",
    "AdoptionSchema"
]
