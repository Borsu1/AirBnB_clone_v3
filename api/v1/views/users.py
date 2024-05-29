#!/usr/bin/python3
"""
This module defines the Flask application and imports the necessary modules.
It also contains the routes for handling User objects.
"""

from flask import Flask, jsonify, abort, request
from models.user import User

app = Flask(__name__)

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """Retrieve a list of all User objects"""
    users = [user.to_dict() for user in User.query.all()]
    return jsonify(users)

@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a specific User object by its ID"""
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a specific User object by its ID"""
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({}), 200

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """Create a new User object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    user = User(email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a specific User object by its ID"""
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    db.session.commit()
    return jsonify(user.to_dict()), 200
