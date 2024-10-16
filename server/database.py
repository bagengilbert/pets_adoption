# server/database.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    """Initialize the database with the given Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets_adoption.db'  # SQLite database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
    app.config['SQLALCHEMY_ECHO'] = True  # Log all SQL statements (optional, for debugging)
    
    db.init_app(app)  # Initialize SQLAlchemy with the app
    migrate.init_app(app, db)  # Initialize Flask-Migrate with the app and db

def create_db(app):
    """Create the database schema."""
    with app.app_context():
        db.create_all()
        print("Database created successfully.")

def drop_db(app):
    """Drop all tables from the database."""
    with app.app_context():
        db.drop_all()
        print("All tables dropped successfully.")

# Add a function to reset the database, if needed
def reset_db(app):
    """Reset the database by dropping and recreating it."""
    drop_db(app)
    create_db(app)
