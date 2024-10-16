# server/resources/adoption_resource.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.adoption import Adoption
from server.models.pet import Pet
from server.schemas.adoption_schema import AdoptionSchema
from server.database import db
from server.logger import logger  # Import the logger

adoption_blueprint = Blueprint('adoption', __name__)
adoption_schema = AdoptionSchema()

@adoption_blueprint.route('/adoptions', methods=['POST'])
@jwt_required()
def adopt_pet():
    """Adopt a pet."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # Fetch the pet to adopt
    pet = Pet.query.get_or_404(data['pet_id'])
    
    # Create a new adoption record
    adoption = Adoption(user_id=user_id, pet_id=pet.id)
    db.session.add(adoption)
    db.session.commit()

    # Log the adoption action
    logger.info(f"User {user_id} adopted pet {pet.id}.")
    return adoption_schema.dump(adoption), 201

@adoption_blueprint.route('/adoptions', methods=['GET'])
@jwt_required()
def get_adoptions():
    """Get all adopted pets for the logged-in user."""
    user_id = get_jwt_identity()
    
    # Retrieve all adoptions for the user
    adoptions = Adoption.query.filter_by(user_id=user_id).all()
    
    # Log the retrieval action
    logger.info(f"User {user_id} retrieved their adoptions.")
    return adoption_schema.dump(adoptions, many=True), 200

@adoption_blueprint.route('/adoptions/<int:adoption_id>', methods=['DELETE'])
@jwt_required()
def delete_adoption(adoption_id):
    """Remove an adoption."""
    adoption = Adoption.query.get_or_404(adoption_id)
    db.session.delete(adoption)
    db.session.commit()

    # Log the deletion action
    logger.info(f"User {get_jwt_identity()} deleted adoption {adoption_id}.")
    return jsonify({"msg": "Adoption deleted"}), 204

@adoption_blueprint.route('/adoptions/<int:adoption_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_adoption(adoption_id):
    """Update adoption details (PUT for full update, PATCH for partial update)."""
    adoption = Adoption.query.get_or_404(adoption_id)
    data = request.get_json()
    
    if request.method == 'PUT':
        # Full update
        adoption.pet_id = data['pet_id']
        logger.info(f"User {get_jwt_identity()} fully updated adoption {adoption_id}.")  # Log the full update
    elif request.method == 'PATCH':
        # Partial update
        if 'pet_id' in data:
            adoption.pet_id = data['pet_id']
            logger.info(f"User {get_jwt_identity()} partially updated adoption {adoption_id}.")  # Log the partial update
    
    db.session.commit()
    return adoption_schema.dump(adoption), 200
