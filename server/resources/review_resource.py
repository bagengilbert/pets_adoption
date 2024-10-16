# server/resources/review_resource.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.review import Review
from server.models.pet import Pet
from server.schemas.review_schema import ReviewSchema
from server.database import db

review_blueprint = Blueprint('review', __name__)
review_schema = ReviewSchema()

@review_blueprint.route('/reviews', methods=['POST'])
@jwt_required()
def add_review():
    """Add a review for a pet."""
    data = request.get_json()
    user_id = get_jwt_identity()
    pet = Pet.query.get_or_404(data['pet_id'])
    
    review = Review(user_id=user_id, pet_id=pet.id, **data)
    db.session.add(review)
    db.session.commit()
    return review_schema.dump(review), 201

@review_blueprint.route('/reviews/<int:pet_id>', methods=['GET'])
def get_pet_reviews(pet_id):
    """Get all reviews for a specific pet."""
    reviews = Review.query.filter_by(pet_id=pet_id).all()
    return review_schema.dump(reviews, many=True), 200

@review_blueprint.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete a review."""
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({"msg": "Review deleted"}), 204

@review_blueprint.route('/reviews/<int:review_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_review(review_id):
    """Update a review (PUT for full update, PATCH for partial update)."""
    review = Review.query.get_or_404(review_id)
    data = request.get_json()
    
    if request.method == 'PUT':
        # Full update
        review.text = data['text']
        review.rating = data['rating']
    elif request.method == 'PATCH':
        # Partial update
        if 'text' in data:
            review.text = data['text']
        if 'rating' in data:
            review.rating = data['rating']
    
    db.session.commit()
    return review_schema.dump(review), 200
