#!/usr/bin/python3
"""
This module defines the Flask application and imports the necessary modules.
It also contains the routes for handling the link between Place and Amenity objects.
"""

from flask import Flask, jsonify, abort, request
from models.place import Place
from models.amenity import Amenity

app = Flask(__name__)

@app.route('/api/v1/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """Retrieve a list of all Amenity objects of a Place"""
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)

@app.route('/api/v1/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Delete a specific Amenity object from a Place"""
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    amenity = Amenity.query.get(amenity_id)
    if amenity is None or amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    db.session.commit()
    return jsonify({}), 200

@app.route('/api/v1/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def add_place_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    amenity = Amenity.query.get(amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    db.session.commit()
    return jsonify(amenity.to_dict()), 201
