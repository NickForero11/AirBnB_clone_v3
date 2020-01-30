"""Module to handle the views of the REST API using blueprints.

Variables:
    app_views (Blueprint): blueprint for the endpoints of the REST API.
"""


from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
