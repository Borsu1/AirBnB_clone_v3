#!/usr/bin/python3
"""
This module defines the Flask application and imports the necessary modules.
It also contains the routes for handling City objects.
"""

from flask import Flask, jsonify, abort, request
from models.state import State
from models.city import City

app = Flask(__name__)

@app.route('/api/v1/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Retrieve a list of all City objects of a State"""
    state = State.query.get(state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app.route('/api/v1/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieve a specific City object by its ID"""
    city = City.query.get(city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app.route('/api/v1/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a specific City object by its ID"""
    city = City.query.get(city_id)
    if city is None:
        abort(404)
    db.session.delete(city)
    db.session.commit()
    return jsonify({}), 200

@app.route('/api/v1/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Create a new City object"""
    state = State.query.get(state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    city = City(name=data['name'], state_id=state.id)
    db.session.add(city)
    db.session.commit()
    return jsonify(city.to_dict()), 201

@app.route('/api/v1/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update a specific City object by its ID"""
    city = City.query.get(city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    db.session.commit()
    return jsonify(city.to_dict()), 200
