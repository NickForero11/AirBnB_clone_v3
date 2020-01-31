#!/usr/bin/python3
"""Module to handle the status endpoint for the REST API.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Handler function for the status endpoint.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    """retrieves the number of each objects by type
    """
    numtype = {"amenities": storage.count("Amenity"),
               "cities": storage.count("City"),
               "places": storage.count("Place"),
               "reviews": storage.count("Review"),
               "states": storage.count("State"),
               "users": storage.count("User")}
    return jsonify(numtype)
