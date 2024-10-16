# server/resources/review_resource.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.review import Review
from server.models.pet import Pet
from server.schemas.review_schema import ReviewSchema
from server.database import db
from server.logger import logger  # Import the logger

review_blueprint = Blueprint('review', __name__)
review_schema = ReviewSchema()

@review_blueprint.route('/reviews', methods=['POST'])
@jwt_required()
def add_review():
    """Add a review for a pet."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    logger.info(f"User {user_id} is attempting to add a review for pet ID: {data['pet_id']}")
    pet = Pet.query.get_or_404(data['pet_id'])
    
    try:
        review = Review(user_id=user_id, pet_id=pet.id, **data)
        db.session.add(review)
        db.session.commit()
        logger.info(f"Review added successfully for pet ID: {pet.id} by user ID: {user_id}")
        return review_schema.dump(review), 201
    except Exception as e:
        logger.error(f"Error adding review for pet ID {pet.id} by user ID {user_id}: {str(e)}")
        return jsonify({"msg": "Error adding review."}), 400

@review_blueprint.route('/reviews/<int:pet_id>', methods=['GET'])
def get_pet_reviews(pet_id):
    """Get all reviews for a specific pet."""
    logger.info(f"Fetching reviews for pet ID: {pet_id}")
    
    reviews = Review.query.filter_by(pet_id=pet_id).all()
    logger.info(f"Total reviews fetched for pet ID {pet_id}: {len(reviews)}")
    return review_schema.dump(reviews, many=True), 200

@review_blueprint.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete a review."""
    logger.info(f"Attempting to delete review ID: {review_id}")
    review = Review.query.get_or_404(review_id)

    try:
        db.session.delete(review)
        db.session.commit()
        logger.info(f"Review deleted successfully: {review_id}")
        return jsonify({"msg": "Review deleted"}), 204
    except Exception as e:
        logger.error(f"Error deleting review ID {review_id}: {str(e)}")
        return jsonify({"msg": "Error deleting review."}), 400

@review_blueprint.route('/reviews/<int:review_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_review(review_id):
    """Update a review (PUT for full update, PATCH for partial update)."""
    logger.info(f"Updating review ID: {review_id}")
    review = Review.query.get_or_404(review_id)
    data = request.get_json()
    
    try:
        if request.method == 'PUT':
            # Full update
            review.text = data['text']
            review.rating = data['rating']
            logger.info(f"Review fully updated for ID: {review_id}")
        elif request.method == 'PATCH':
            # Partial update
            if 'text' in data:
                review.text = data['text']
                logger.info(f"Review text updated for ID: {review_id}")
            if 'rating' in data:
                review.rating = data['rating']
                logger.info(f"Review rating updated for ID: {review_id}")
        
        db.session.commit()
        return review_schema.dump(review), 200
    except Exception as e:
        logger.error(f"Error updating review ID {review_id}: {str(e)}")
        return jsonify({"msg": "Error updating review."}), 400
