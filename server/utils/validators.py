# server/utils/validators.py

import re
from marshmallow import ValidationError

def validate_positive_integer(value):
    """Ensure the value is a positive integer."""
    if not isinstance(value, int) or value < 0:
        raise ValidationError("Value must be a positive integer.")

def validate_non_empty_string(value):
    """Ensure the string is non-empty."""
    if not value or not isinstance(value, str):
        raise ValidationError("Value must be a non-empty string.")

def validate_url(url):
    """Basic URL validation."""
    url_regex = r'^(http|https)://[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})'
    if not re.match(url_regex, url):
        raise ValidationError("Invalid URL format.")

def validate_email(email):
    """Validate an email address."""
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise ValidationError("Invalid email format.")
