#!/usr/bin/python3
"""
This module defines the Flask application and imports the necessary modules.
It also contains the routes for handling Amenity objects.
"""

from flask import Flask, jsonify, abort, request
from models.amenity import Amenity

app = Flask(__name__)

@app.route('/api/v1/amenities', methods=['GET'])
def get_amenities():
    """Retrieve a list of all Amenity objects"""
    amenities = [amenity.to_dict() for amenity in Amenity.query.all()]
    return jsonify(amenities)

@app.route('/api/v1/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieve a specific Amenity object by its ID"""
    amenity = Amenity.query.get(amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete a specific Amenity object by its ID"""
    amenity = Amenity.query.get(amenity_id)
    if amenity is None:
        abort(404)
    db.session.delete(amenity)
    db.session.commit()
    return jsonify({}), 200

@app.route('/api/v1/amenities', methods=['POST'])
def create_amenity():
    """Create a new Amenity object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    amenity = Amenity(name=data['name'])
    db.session.add(amenity)
    db.session.commit()
    return jsonify(amenity.to_dict()), 201

@app.route('/api/v1/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update a specific Amenity object by its ID"""
    amenity = Amenity.query.get(amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    db.session.commit()
    return jsonify(amenity.to_dict()), 200
