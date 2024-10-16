# server/logger.py

import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(app):
    """Set up logging for the Flask app."""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create a rotating file handler
    handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=10 * 1024 * 1024,  # 10 MB per file
        backupCount=5                # Keep 5 backup files
    )
    handler.setLevel(logging.INFO)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Set up logging for the app
    app.logger.addHandler(handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)  # Set the log level for the app

    # Example log message
    app.logger.info('Logger has been set up.')

