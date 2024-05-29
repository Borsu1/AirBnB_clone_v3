#!/usr/bin/python3
"""
This module defines the Flask application and imports the necessary modules.
It also contains the routes for handling Review objects.
"""

from flask import Flask, jsonify, abort, request
from models.place import Place
from models.user import User
from models.review import Review

app = Flask(__name__)

@app.route('/api/v1/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """Retrieve a list of all Review objects of a Place"""
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app.route('/api/v1/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieve a specific Review object by its ID"""
    review = Review.query.get(review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app.route('/api/v1/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a specific Review object by its ID"""
    review = Review.query.get(review_id)
    if review is None:
        abort(404)
    db.session.delete(review)
    db.session.commit()
    return jsonify({}), 200

@app.route('/api/v1/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Create a new Review object"""
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = User.query.get(data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, description="Missing text")
    review = Review(text=data['text'], place_id=place.id, user_id=user.id)
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201

@app.route('/api/v1/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Update a specific Review object by its ID"""
    review = Review.query.get(review_id)
    if review is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    db.session.commit()
    return jsonify(review.to_dict()), 200
