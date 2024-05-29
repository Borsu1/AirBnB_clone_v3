#!/usr/bin/python3
"""
This module defines the Flask application and imports the necessary modules.
It also contains the routes for handling Place objects.
"""

from flask import Flask, jsonify, abort, request
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)

@app.route('/api/v1/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Retrieve a list of all Place objects of a City"""
    city = City.query.get(city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app.route('/api/v1/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieve a specific Place object by its ID"""
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app.route('/api/v1/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a specific Place object by its ID"""
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    db.session.delete(place)
    db.session.commit()
    return jsonify({}), 200

@app.route('/api/v1/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create a new Place object"""
    city = City.query.get(city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = User.query.get(data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    place = Place(name=data['name'], city_id=city.id, user_id=user.id)
    db.session.add(place)
    db.session.commit()
    return jsonify(place.to_dict()), 201

@app.route('/api/v1/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a specific Place object by its ID"""
    place = Place.query.get(place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    db.session.commit()
    return jsonify(place.to_dict()), 200

@app.route('/api/v1/places_search', methods=['POST'])
def places_search():
    """
    This function retrieves all Place objects depending on the JSON in the body of the request.
    """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not states and not cities and not amenities:
        places = Place.query.all()
    else:
        places = []

        for state_id in states:
            state = State.query.get(state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        if place not in places:
                            places.append(place)

        for city_id in cities:
            city = City.query.get(city_id)
            if city:
                for place in city.places:
                    if place not in places:
                        places.append(place)

        if amenities:
            places = [place for place in places 
                      if all(amenity.id in place.amenities 
                             for amenity in amenities)]

    return jsonify([place.to_dict() for place in places]), 200
