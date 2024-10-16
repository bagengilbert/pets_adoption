from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from server.config import DevelopmentConfig  # Ensure the import path is correct
from server.resources import register_routes  # Ensure the import path is correct

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Load configuration
app.config.from_object(DevelopmentConfig)  # Load the config from the class

# Initialize the database
db = SQLAlchemy(app)

# Register the API routes
register_routes(app)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Set debug=False in production
