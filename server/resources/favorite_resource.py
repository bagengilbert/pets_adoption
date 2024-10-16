# server/resources/favorite_resource.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.favorite import Favorite
from server.models.pet import Pet
from server.schemas.favorite_schema import FavoriteSchema
from server.database import db

favorite_blueprint = Blueprint('favorite', __name__)
favorite_schema = FavoriteSchema(many=True)

@favorite_blueprint.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    """Add a pet to favorites."""
    data = request.get_json()
    user_id = get_jwt_identity()
    pet = Pet.query.get_or_404(data['pet_id'])
    
    favorite = Favorite(user_id=user_id, pet_id=pet.id)
    db.session.add(favorite)
    db.session.commit()
    return favorite_schema.dump(favorite), 201

@favorite_blueprint.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    """Get all favorite pets for the logged-in user."""
    user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return favorite_schema.dump(favorites), 200

@favorite_blueprint.route('/favorites/<int:fav_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(fav_id):
    """Remove a pet from favorites."""
    favorite = Favorite.query.get_or_404(fav_id)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 204

@favorite_blueprint.route('/favorites/<int:fav_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_favorite(fav_id):
    """Update a favorite pet (PUT for full update, PATCH for partial update)."""
    favorite = Favorite.query.get_or_404(fav_id)
    data = request.get_json()
    
    if request.method == 'PUT':
        # Full update
        favorite.pet_id = data['pet_id']
    elif request.method == 'PATCH':
        # Partial update
        if 'pet_id' in data:
            favorite.pet_id = data['pet_id']
    
    db.session.commit()
    return favorite_schema.dump(favorite), 200
