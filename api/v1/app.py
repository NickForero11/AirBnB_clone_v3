#!/usr/bin/python3
"""Module that starts a Flask app that handles the REST API.
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_handler(err):
    """Handler for the close of the application context.
    """
    storage.close()


host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

if __name__ == '__main__':
    app.run(host, port, threaded=True)
