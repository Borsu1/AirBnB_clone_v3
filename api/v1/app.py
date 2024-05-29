#!/usr/bin/python3
"""
This module defines the Flask application.

The application is defined as a Flask instance. It includes the setup for
different routes and error handlers.
"""

from flask import Flask, jsonify
import os

from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(error):
    """
    This function is called when a 404 error occurs.
    Args:
      error (Exception): The error that caused the 404.
    Returns:
        A JSON response with the content {"error": "Not found"}
        and a ststus code of 404.
    """ 
 return jsonify({"error": "Not found"}), 404

@app.teardown_appcontext
def close_db(error):
    """
    This function is called when the Flask application context is torn down.

    Args:
        error (Exception): The error that caused the context teardown, if any.

    It closes the storage system session.
    """
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
