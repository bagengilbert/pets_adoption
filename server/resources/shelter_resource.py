# server/resources/shelter_resource.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.shelter import Shelter
from server.schemas.shelter_schema import ShelterSchema
from server.database import db

shelter_blueprint = Blueprint('shelter', __name__)
shelter_schema = ShelterSchema()

@shelter_blueprint.route('/shelters', methods=['POST'])
@jwt_required()
def add_shelter():
    """Add a new shelter."""
    data = request.get_json()
    shelter = shelter_schema.load(data)  # Validate and deserialize input
    db.session.add(shelter)
    db.session.commit()
    return shelter_schema.dump(shelter), 201

@shelter_blueprint.route('/shelters', methods=['GET'])
def get_shelters():
    """Get all shelters."""
    shelters = Shelter.query.all()
    return shelter_schema.dump(shelters, many=True), 200

@shelter_blueprint.route('/shelters/<int:shelter_id>', methods=['GET'])
def get_shelter(shelter_id):
    """Get details of a specific shelter."""
    shelter = Shelter.query.get_or_404(shelter_id)
    return shelter_schema.dump(shelter), 200

@shelter_blueprint.route('/shelters/<int:shelter_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_shelter(shelter_id):
    """Update a shelter's details (PUT for full update, PATCH for partial update)."""
    shelter = Shelter.query.get_or_404(shelter_id)
    data = request.get_json()
    
    if request.method == 'PUT':
        # Full update
        shelter.name = data['name']
        shelter.location = data['location']
        shelter.contact_info = data['contact_info']
    elif request.method == 'PATCH':
        # Partial update
        if 'name' in data:
            shelter.name = data['name']
        if 'location' in data:
            shelter.location = data['location']
        if 'contact_info' in data:
            shelter.contact_info = data['contact_info']
    
    db.session.commit()
    return shelter_schema.dump(shelter), 200

@shelter_blueprint.route('/shelters/<int:shelter_id>', methods=['DELETE'])
@jwt_required()
def delete_shelter(shelter_id):
    """Delete a shelter."""
    shelter = Shelter.query.get_or_404(shelter_id)
    db.session.delete(shelter)
    db.session.commit()
    return jsonify({"msg": "Shelter deleted"}), 204
