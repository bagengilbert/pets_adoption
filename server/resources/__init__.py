# server/resources/__init__.py

from .adoption_resource import adoption_blueprint
from .favorite_resource import favorite_blueprint
from .pet_resource import pet_blueprint
from .review_resource import review_blueprint
from .shelter_resource import shelter_blueprint
from .user_resource import user_blueprint

# You can also create a list of blueprints to register them in your main application
blueprints = [
    adoption_blueprint,
    favorite_blueprint,
    pet_blueprint,
    review_blueprint,
    shelter_blueprint,
    user_blueprint,
]
