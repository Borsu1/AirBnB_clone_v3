#!/usr/bin/python3
"""
This module sets up the default route and additional routes for the API.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'])
def status():
    """
    This function handles the route /status and returns a JSON response.
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """
    This function handles the route /stats and returns a JSON response with the
    count of each object by type.
    """
    return jsonify({
        "users": storage.count("User"),
        "places": storage.count("Place"),
        "cities": storage.count("City"),
        "states": storage.count("State"),
        "amenities": storage.count("Amenity"),
        "reviews": storage.count("Review")
    })
