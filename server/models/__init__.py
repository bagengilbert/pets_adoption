# server/models/__init__.py

from .user import User
from .pet import Pet
from .favorite import Favorite
from .adoption import Adoption
from .review import Review
from .shelter import Shelter

#create a list of all models needed for imports elsewhere
__all__ = [
    "User",
    "Pet",
    "Favorite",
    "Adoption",
    "Review",
    "Shelter"
]
