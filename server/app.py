# server/app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from server.config import config
from server.logger import setup_logger  # Import the setup_logger function

# Import resources
from server.resources.user_resource import user_blueprint
from server.resources.pet_resource import pet_blueprint
from server.resources.favorite_resource import favorite_blueprint
from server.resources.adoption_resource import adoption_blueprint
from server.resources.review_resource import review_blueprint
from server.resources.shelter_resource import shelter_blueprint

# Initialize Flask application
app = Flask(__name__)

# Load configuration
app.config.from_object(config)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Set up logging
setup_logger(app)  # Pass the app instance to the logger setup function

# Register API resources
@app.route('/api')
def index():
    return {"message": "Welcome to the PETS_ADOPTION API"}

# Registering user, pet, favorite pet, adoption, review, and shelter resources
app.register_blueprint(user_blueprint, url_prefix='/api/users')
app.register_blueprint(pet_blueprint, url_prefix='/api/pets')
app.register_blueprint(favorite_blueprint, url_prefix='/api/favorite_pets')
app.register_blueprint(adoption_blueprint, url_prefix='/api/adoptions')
app.register_blueprint(review_blueprint, url_prefix='/api/reviews')
app.register_blueprint(shelter_blueprint, url_prefix='/api/shelters')

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
