# server/resources/shelter_resource.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.shelter import Shelter
from server.schemas.shelter_schema import ShelterSchema
from server.database import db
from server.logger import logger  # Import the logger

shelter_blueprint = Blueprint('shelter', __name__)
shelter_schema = ShelterSchema()

@shelter_blueprint.route('/shelters', methods=['POST'])
@jwt_required()
def add_shelter():
    """Add a new shelter."""
    data = request.get_json()
    logger.info("Attempting to add a new shelter.")

    try:
        shelter = shelter_schema.load(data)  # Validate and deserialize input
        db.session.add(shelter)
        db.session.commit()
        logger.info(f"Shelter added successfully: {shelter.name}")
        return shelter_schema.dump(shelter), 201
    except Exception as e:
        logger.error(f"Error adding shelter: {str(e)}")
        return jsonify({"msg": "Error adding shelter."}), 400

@shelter_blueprint.route('/shelters', methods=['GET'])
def get_shelters():
    """Get all shelters."""
    logger.info("Fetching all shelters.")
    
    shelters = Shelter.query.all()
    logger.info(f"Total shelters fetched: {len(shelters)}")
    return shelter_schema.dump(shelters, many=True), 200

@shelter_blueprint.route('/shelters/<int:shelter_id>', methods=['GET'])
def get_shelter(shelter_id):
    """Get details of a specific shelter."""
    logger.info(f"Fetching details for shelter ID: {shelter_id}")
    
    shelter = Shelter.query.get_or_404(shelter_id)
    logger.info(f"Shelter details fetched successfully for ID: {shelter_id}")
    return shelter_schema.dump(shelter), 200

@shelter_blueprint.route('/shelters/<int:shelter_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_shelter(shelter_id):
    """Update a shelter's details (PUT for full update, PATCH for partial update)."""
    logger.info(f"Updating shelter ID: {shelter_id}")
    shelter = Shelter.query.get_or_404(shelter_id)
    data = request.get_json()
    
    try:
        if request.method == 'PUT':
            # Full update
            shelter.name = data['name']
            shelter.location = data['location']
            shelter.contact_info = data['contact_info']
            logger.info(f"Shelter fully updated: {shelter.name}")
        elif request.method == 'PATCH':
            # Partial update
            if 'name' in data:
                shelter.name = data['name']
            if 'location' in data:
                shelter.location = data['location']
            if 'contact_info' in data:
                shelter.contact_info = data['contact_info']
            logger.info(f"Shelter partially updated for ID: {shelter_id}")

        db.session.commit()
        return shelter_schema.dump(shelter), 200
    except Exception as e:
        logger.error(f"Error updating shelter ID {shelter_id}: {str(e)}")
        return jsonify({"msg": "Error updating shelter."}), 400

@shelter_blueprint.route('/shelters/<int:shelter_id>', methods=['DELETE'])
@jwt_required()
def delete_shelter(shelter_id):
    """Delete a shelter."""
    logger.info(f"Attempting to delete shelter ID: {shelter_id}")
    shelter = Shelter.query.get_or_404(shelter_id)

    try:
        db.session.delete(shelter)
        db.session.commit()
        logger.info(f"Shelter deleted successfully: {shelter.name}")
        return jsonify({"msg": "Shelter deleted"}), 204
    except Exception as e:
        logger.error(f"Error deleting shelter ID {shelter_id}: {str(e)}")
        return jsonify({"msg": "Error deleting shelter."}), 400
