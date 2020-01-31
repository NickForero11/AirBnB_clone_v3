#!/usr/bin/python3
"""Module that starts a Flask app that handles the REST API."""
from flask import (Flask, jsonify)
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
cors_conf = {'resources': r'/*', 'origins': '0.0.0.0'}
CORS(app, **cors_conf)


@app.teardown_appcontext
def teardown_handler(err):
    """Handler for the close of the application context.

    Decorators:
        app.teardown_appcontext

    Arguments:
        err (Exception):  The response that object that contains the exception
                          and important information, e.g. its HTTP error code.
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """Handler for a HTTP Request not found error in the REST API.

    Decorators:
        app.errorhandler

    Arguments:
        err (Exception):  The response that object that contains the exception
                          and important information, e.g. its HTTP error code.

    Returns:
         BaseResponse:  The JSON representation of the API response
                        for a 404 HTTP error code.
    """
    return (jsonify({"error": "Not found"}), 404)


host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

if __name__ == '__main__':
    app.run(host, port, threaded=True)
