"""Module to handle the status endpoint for the REST API.
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Handler function for the status endpoint.
    """
    return jsonify({"status": "OK"})
