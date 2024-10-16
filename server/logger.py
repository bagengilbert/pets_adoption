# server/logger.py

import logging

def setup_logger(app=None):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(ch)

    if app:
        # Optionally attach the logger to the Flask app if needed
        app.logger.addHandler(ch)

    return logger

# Instantiate the logger
logger = setup_logger()
