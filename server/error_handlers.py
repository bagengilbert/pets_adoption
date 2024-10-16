# server/error_handlers.py

from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """Register error handlers for the Flask app."""
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle HTTP exceptions."""
        response = jsonify({
            "error": {
                "code": error.code,
                "name": error.name,
                "description": error.description,
            }
        })
        response.status_code = error.code
        return response

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle non-HTTP exceptions."""
        response = jsonify({
            "error": {
                "code": 500,
                "name": "Internal Server Error",
                "description": "An unexpected error occurred."
            }
        })
        response.status_code = 500
        return response

    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors."""
        response = jsonify({
            "error": {
                "code": 404,
                "name": "Not Found",
                "description": "The requested resource was not found."
            }
        })
        response.status_code = 404
        return response

    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle 400 errors."""
        response = jsonify({
            "error": {
                "code": 400,
                "name": "Bad Request",
                "description": "The request was malformed or invalid."
            }
        })
        response.status_code = 400
        return response

    @app.errorhandler(401)
    def handle_unauthorized(error):
        """Handle 401 errors."""
        response = jsonify({
            "error": {
                "code": 401,
                "name": "Unauthorized",
                "description": "Authentication is required and has failed or has not yet been provided."
            }
        })
        response.status_code = 401
        return response

    @app.errorhandler(403)
    def handle_forbidden(error):
        """Handle 403 errors."""
        response = jsonify({
            "error": {
                "code": 403,
                "name": "Forbidden",
                "description": "You do not have permission to access this resource."
            }
        })
        response.status_code = 403
        return response
