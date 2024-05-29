#!/usr/bin/python3
"""
This module defines the Flask application and imports the necessary modules.
"""


from flask import Flask, jsonify, abort, request
from models.state import State

app = Flask(__name__)

@app.route('/api/v1/states', methods=['GET'])
def get_states():
    """Retrieve a list of all State objects"""
    states = [state.to_dict() for state in State.query.all()]
    return jsonify(states)

@app.route('/api/v1/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieve a specific State object by its ID"""
    state = State.query.get(state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a specific State object by its ID"""
    state = State.query.get(state_id)
    if state is None:
        abort(404)
    db.session.delete(state)
    db.session.commit()
    return jsonify({}), 200

@app.route('/api/v1/states', methods=['POST'])
def create_state():
    """Create a new State object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    state = State(name=data['name'])
    db.session.add(state)
    db.session.commit()
    return jsonify(state.to_dict()), 201

@app.route('/api/v1/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a specific State object by its ID"""
    state = State.query.get(state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    db.session.commit()
    return jsonify(state.to_dict()), 200
