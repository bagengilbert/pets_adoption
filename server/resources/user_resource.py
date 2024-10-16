# server/resources/user_resource.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from server.models.user import User
from server.schemas.user_schema import UserSchema
from server.database import db

user_blueprint = Blueprint('user', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_blueprint.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    user = user_schema.load(data)  # Validate and deserialize input
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201

@user_blueprint.route('/login', methods=['POST'])
def login():
    """Login a user and return a JWT token."""
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad email or password"}), 401

@user_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Get the logged-in user's profile."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user_schema.dump(user), 200

@user_blueprint.route('/profile', methods=['PUT', 'PATCH'])
@jwt_required()
def update_profile():
    """Update the logged-in user's profile (PUT for full update, PATCH for partial update)."""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if request.method == 'PUT':
        # Full update
        user.email = data['email']
        user.password = data['password']  # Ensure you handle password hashing in the User model
    elif request.method == 'PATCH':
        # Partial update
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = data['password']  # Ensure you handle password hashing in the User model
    
    db.session.commit()
    return user_schema.dump(user), 200
