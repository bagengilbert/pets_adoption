from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import logging
from logging.handlers import RotatingFileHandler
from server.config import config
from server.models.user import User
from server.models.pet import Pet
from server.models.favorite_pet import FavoritePet
from server.models.adoption import Adoption
from server.models.review import Review
from server.models.shelter import Shelter
from server.resources.user_resource import UserResource
from server.resources.pet_resource import PetResource
from server.resources.favorite_pet_resource import FavoritePetResource
from server.resources.adoption_resource import AdoptionResource
from server.resources.review_resource import ReviewResource
from server.resources.shelter_resource import ShelterResource

# Initialize Flask application
app = Flask(__name__)

# Load configuration
app.config.from_object(config)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Set up logging
if not app.debug:
    handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10000, backupCount=1)
    handler.setLevel(app.config['LOG_LEVEL'])
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

# Register API resources
@app.route('/api')
def index():
    return {"message": "Welcome to the PETS_ADOPTION API"}

# Registering user, pet, favorite pet, adoption, review, and shelter resources
app.add_url_rule('/api/users', view_func=UserResource.as_view('user_resource'))
app.add_url_rule('/api/pets', view_func=PetResource.as_view('pet_resource'))
app.add_url_rule('/api/favorite_pets', view_func=FavoritePetResource.as_view('favorite_pet_resource'))
app.add_url_rule('/api/adoptions', view_func=AdoptionResource.as_view('adoption_resource'))
app.add_url_rule('/api/reviews', view_func=ReviewResource.as_view('review_resource'))
app.add_url_rule('/api/shelters', view_func=ShelterResource.as_view('shelter_resource'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {"error": "Resource not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal error: {error}")
    return {"error": "An internal error occurred"}, 500

# Create the database and tables if they do not exist
@app.before_first_request
def create_tables():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Set debug to False in production
