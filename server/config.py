import os

class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', '2cd748e8306e84f64599459b6cbd78af')  # Use a secure key for production

    # Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids overhead
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')  # Default to SQLite


class DevelopmentConfig(Config):
    """Development configuration class."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')  # SQLite for dev


class TestingConfig(Config):
    """Testing configuration class."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite3'  # Use a separate SQLite database for tests


class ProductionConfig(Config):
    """Production configuration class."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')  # Use your production database URL
