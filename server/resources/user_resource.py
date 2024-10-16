# server/resources/user_resource.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from server.models.user import User
from server.schemas.user_schema import UserSchema
from server.database import db
from server.logger import logger  # Import the logger

user_blueprint = Blueprint('user', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_blueprint.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    logger.info("Attempting to register a new user.")

    try:
        user = user_schema.load(data)  # Validate and deserialize input
        db.session.add(user)
        db.session.commit()
        logger.info(f"User registered successfully: {user.email}")
        return user_schema.dump(user), 201
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        return jsonify({"msg": "Error registering user."}), 400

@user_blueprint.route('/login', methods=['POST'])
def login():
    """Login a user and return a JWT token."""
    data = request.get_json()
    logger.info("Attempting to log in user.")

    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        logger.info(f"User logged in successfully: {user.email}")
        return jsonify(access_token=access_token), 200
    
    logger.warning(f"Failed login attempt for email: {data['email']}")
    return jsonify({"msg": "Bad email or password"}), 401

@user_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Get the logged-in user's profile."""
    user_id = get_jwt_identity()
    logger.info(f"Fetching profile for user ID: {user_id}")

    user = User.query.get(user_id)
    if user:
        logger.info(f"Profile fetched successfully for user ID: {user_id}")
        return user_schema.dump(user), 200
    else:
        logger.warning(f"User not found for ID: {user_id}")
        return jsonify({"msg": "User not found"}), 404

@user_blueprint.route('/profile', methods=['PUT', 'PATCH'])
@jwt_required()
def update_profile():
    """Update the logged-in user's profile (PUT for full update, PATCH for partial update)."""
    user_id = get_jwt_identity()
    logger.info(f"Updating profile for user ID: {user_id}")

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    try:
        if request.method == 'PUT':
            # Full update
            user.email = data['email']
            user.password = data['password']  # Ensure you handle password hashing in the User model
            logger.info(f"User profile fully updated: {user.email}")
        elif request.method == 'PATCH':
            # Partial update
            if 'email' in data:
                user.email = data['email']
            if 'password' in data:
                user.password = data['password']  # Ensure you handle password hashing in the User model
            logger.info(f"User profile partially updated for user ID: {user_id}")

        db.session.commit()
        return user_schema.dump(user), 200
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        return jsonify({"msg": "Error updating user profile."}), 400
