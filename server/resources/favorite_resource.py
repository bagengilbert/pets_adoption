# server/resources/favorite_resource.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.favorite import Favorite
from server.models.pet import Pet
from server.schemas.favorite_schema import FavoriteSchema
from server.database import db
from server.logger import logger  # Import the logger

favorite_blueprint = Blueprint('favorite', __name__)
favorite_schema = FavoriteSchema()

@favorite_blueprint.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    """Add a pet to favorites."""
    data = request.get_json()
    user_id = get_jwt_identity()  # Get the user ID from the JWT
    logger.info(f"User {user_id} is attempting to add a favorite pet.")

    pet = Pet.query.get_or_404(data['pet_id'])
    
    favorite = Favorite(user_id=user_id, pet_id=pet.id)

    try:
        db.session.add(favorite)
        db.session.commit()
        logger.info(f"Pet ID {pet.id} added to favorites by user ID {user_id}.")
        return favorite_schema.dump(favorite), 201
    except Exception as e:
        logger.error(f"Error adding pet ID {pet.id} to favorites for user ID {user_id}: {str(e)}")
        return jsonify({"msg": "Error adding favorite."}), 400

@favorite_blueprint.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    """Get all favorite pets for the logged-in user."""
    user_id = get_jwt_identity()
    logger.info(f"Fetching favorites for user ID: {user_id}")

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return favorite_schema.dump(favorites), 200

@favorite_blueprint.route('/favorites/<int:fav_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(fav_id):
    """Remove a pet from favorites."""
    logger.info(f"User is attempting to delete favorite ID: {fav_id}")
    favorite = Favorite.query.get_or_404(fav_id)

    try:
        db.session.delete(favorite)
        db.session.commit()
        logger.info(f"Favorite ID {fav_id} deleted successfully.")
        return jsonify({"msg": "Favorite deleted"}), 204
    except Exception as e:
        logger.error(f"Error deleting favorite ID {fav_id}: {str(e)}")
        return jsonify({"msg": "Error deleting favorite."}), 400

@favorite_blueprint.route('/favorites/<int:fav_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_favorite(fav_id):
    """Update a favorite pet (PUT for full update, PATCH for partial update)."""
    logger.info(f"Updating favorite ID: {fav_id}")
    favorite = Favorite.query.get_or_404(fav_id)
    data = request.get_json()

    try:
        if request.method == 'PUT':
            # Full update
            favorite.pet_id = data['pet_id']
            logger.info(f"Favorite ID {fav_id} fully updated to pet ID {data['pet_id']}.")
        elif request.method == 'PATCH':
            # Partial update
            if 'pet_id' in data:
                favorite.pet_id = data['pet_id']
                logger.info(f"Favorite ID {fav_id} partially updated to pet ID {data['pet_id']}.")

        db.session.commit()
        return favorite_schema.dump(favorite), 200
    except Exception as e:
        logger.error(f"Error updating favorite ID {fav_id}: {str(e)}")
        return jsonify({"msg": "Error updating favorite."}), 400
