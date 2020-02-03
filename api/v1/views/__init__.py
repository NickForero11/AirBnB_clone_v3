#!/usr/bin/python3
"""Module to handle the views of the REST API using blueprints.
Variables:
    app_views (Blueprint): blueprint for the endpoints of the REST API.
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
