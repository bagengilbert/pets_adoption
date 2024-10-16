# server/resources/pet_resource.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.pet import Pet
from server.schemas.pet_schema import PetSchema
from server.database import db

pet_blueprint = Blueprint('pet', __name__)
pet_schema = PetSchema()
pets_schema = PetSchema(many=True)

@pet_blueprint.route('/pets', methods=['POST'])
@jwt_required()
def add_pet():
    """Add a new pet."""
    data = request.get_json()
    pet = pet_schema.load(data)  # Validate and deserialize input
    user_id = get_jwt_identity()
    pet.user_id = user_id  # Associate pet with the logged-in user
    db.session.add(pet)
    db.session.commit()
    return pet_schema.dump(pet), 201

@pet_blueprint.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    """Get a specific pet by ID."""
    pet = Pet.query.get_or_404(pet_id)
    return pet_schema.dump(pet), 200

@pet_blueprint.route('/pets/<int:pet_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_pet(pet_id):
    """Update a pet's details (PUT for full update, PATCH for partial update)."""
    pet = Pet.query.get_or_404(pet_id)
    data = request.get_json()
    
    if request.method == 'PUT':
        # Full update
        pet_schema.load(data, instance=pet)  # Replace with the new data
    elif request.method == 'PATCH':
        # Partial update
        pet_schema.load(data, instance=pet, partial=True)  # Only update specified fields
    
    db.session.commit()
    return pet_schema.dump(pet), 200

@pet_blueprint.route('/pets/<int:pet_id>', methods=['DELETE'])
@jwt_required()
def delete_pet(pet_id):
    """Delete a pet."""
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    return jsonify({"msg": "Pet deleted"}), 204
