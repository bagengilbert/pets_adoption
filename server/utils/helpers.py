# server/utils/helpers.py

from flask import request
import re
import random
import string
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_request_json():
    """Return the JSON data from the request."""
    if request.is_json:
        logger.info("Received JSON request.")
        return request.get_json()
    logger.warning("Request is not JSON.")
    return {}

def validate_email(email):
    """Validate an email address format."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    is_valid = re.match(email_regex, email) is not None
    logger.debug(f"Email validation for '{email}': {is_valid}")
    return is_valid

def generate_random_string(length=8):
    """Generate a random string of a given length."""
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    logger.info(f"Generated random string: {random_string}")
    return random_string

def log_request_info():
    """Log information about the incoming request."""
    logger.info(f"Request Path: {request.path}")
    logger.info(f"Request Method: {request.method}")
    logger.info(f"Request Body: {request.get_json()}")
