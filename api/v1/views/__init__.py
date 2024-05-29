#!/usr/bin/python3
"""
This module initializes the views package and sets up the blueprint for the API.
"""

from flask import Blueprint
from . import states, cities, amenities, users, places, places_reviews, places_amenities

# Create an instance of Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of everything in the package api.v1.views.index
# PEP8 will complain about it, don’t worry, it’s normal and this file won’t be checked.
from api.v1.views import *
