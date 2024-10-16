# server/constants.py

# Status Codes
HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_NO_CONTENT = 204
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_FORBIDDEN = 403
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_CONFLICT = 409
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500

# Error Messages
ERROR_USER_NOT_FOUND = "User not found."
ERROR_INVALID_CREDENTIALS = "Invalid email or password."
ERROR_PET_NOT_FOUND = "Pet not found."
ERROR_ADOPTION_NOT_FOUND = "Adoption record not found."
ERROR_REVIEW_NOT_FOUND = "Review not found."
ERROR_FAVORITE_NOT_FOUND = "Favorite pet not found."
ERROR_SHELTER_NOT_FOUND = "Shelter not found."
ERROR_INVALID_INPUT = "Invalid input provided."

# Validation Messages
VALIDATION_EMAIL_INVALID = "Email address is invalid."
VALIDATION_STRING_EMPTY = "This field cannot be empty."
VALIDATION_INTEGER_POSITIVE = "Value must be a positive integer."
VALIDATION_URL_INVALID = "Invalid URL format."

# General Constants
MAX_PET_IMAGE_SIZE_MB = 5  # Max pet image size in MB
JWT_EXPIRATION_DELTA = 60 * 60  # Token expiration in seconds (1 hour)
PASSWORD_MIN_LENGTH = 8  # Minimum password length
PASSWORD_COMPLEXITY_REGEX = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'  # At least one letter and one number

# Other Constants
DEFAULT_PAGE_SIZE = 10  # Default number of items per page
MAX_PAGE_SIZE = 100  # Maximum number of items per page
