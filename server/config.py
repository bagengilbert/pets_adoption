import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Ensure you set this in your .env file
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications for performance
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret')  # Ensure you set this in your .env file
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # Default log level
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')  # Log file name

class DevelopmentConfig(Config):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///dev.db')  # Default SQLite for dev

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///test.db')  # Default SQLite for testing
    PRESERVE_CONTEXT_ON_EXCEPTION = False  # Disable for easier testing

class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Production database URL (set in .env)
    
# Dictionary to select the appropriate configuration based on environment
config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig
}

# Default configuration
config = config_by_name[os.getenv('FLASK_ENV', 'dev')]
