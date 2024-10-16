# server/resources/pet_resource.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.pet import Pet
from server.schemas.pet_schema import PetSchema
from server.database import db
from server.logger import logger  # Import the logger

pet_blueprint = Blueprint('pet', __name__)
pet_schema = PetSchema()
pets_schema = PetSchema(many=True)

@pet_blueprint.route('/pets', methods=['POST'])
@jwt_required()
def add_pet():
    """Add a new pet."""
    data = request.get_json()
    user_id = get_jwt_identity()  # Get the user ID from the JWT
    logger.info(f"User {user_id} is attempting to add a new pet.")
    
    pet = pet_schema.load(data)  # Validate and deserialize input
    pet.user_id = user_id  # Associate pet with the logged-in user

    try:
        db.session.add(pet)
        db.session.commit()
        logger.info(f"Pet added successfully: {pet.id} by user ID: {user_id}")
        return pet_schema.dump(pet), 201
    except Exception as e:
        logger.error(f"Error adding pet by user ID {user_id}: {str(e)}")
        return jsonify({"msg": "Error adding pet."}), 400

@pet_blueprint.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    """Get a specific pet by ID."""
    logger.info(f"Fetching pet ID: {pet_id}")
    pet = Pet.query.get_or_404(pet_id)
    return pet_schema.dump(pet), 200

@pet_blueprint.route('/pets/<int:pet_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_pet(pet_id):
    """Update a pet's details (PUT for full update, PATCH for partial update)."""
    logger.info(f"Updating pet ID: {pet_id}")
    pet = Pet.query.get_or_404(pet_id)
    data = request.get_json()

    try:
        if request.method == 'PUT':
            # Full update
            pet_schema.load(data, instance=pet)  # Replace with the new data
            logger.info(f"Pet fully updated: {pet.id}")
        elif request.method == 'PATCH':
            # Partial update
            pet_schema.load(data, instance=pet, partial=True)  # Only update specified fields
            logger.info(f"Pet partially updated: {pet.id}")

        db.session.commit()
        return pet_schema.dump(pet), 200
    except Exception as e:
        logger.error(f"Error updating pet ID {pet_id}: {str(e)}")
        return jsonify({"msg": "Error updating pet."}), 400

@pet_blueprint.route('/pets/<int:pet_id>', methods=['DELETE'])
@jwt_required()
def delete_pet(pet_id):
    """Delete a pet."""
    logger.info(f"Attempting to delete pet ID: {pet_id}")
    pet = Pet.query.get_or_404(pet_id)

    try:
        db.session.delete(pet)
        db.session.commit()
        logger.info(f"Pet deleted successfully: {pet.id}")
        return jsonify({"msg": "Pet deleted"}), 204
    except Exception as e:
        logger.error(f"Error deleting pet ID {pet_id}: {str(e)}")
        return jsonify({"msg": "Error deleting pet."}), 400
