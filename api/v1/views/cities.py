#!/usr/bin/python3
"""Module to handle all the default RestFul API actions for City objects.
"""
from api.v1.views import app_views
from flask import (jsonify, request, abort)
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """Handler for the HTTP GET method for cities in a state.

    Decorators:
        app_views.route

    Arguments:
        state_id (str):  The unique ID value of the state.

    Returns:
         response:  The JSON representation of the API response
                    containing the cities in the specificated state.
    """
    states = storage.all("State")
    city_state_key = [key for key in states.keys()
                      if key.split('.')[-1] == state_id]
    if city_state_key:
        key = city_state_key[0]
        list_cities = states.get(key).cities
        response = [city.to_dict() for city in list_cities]
        return jsonify(response)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Handler for the HTTP GET method for a city by its ID.

    Decorators:
        app_views.route

    Arguments:
        city_id (str):  The unique ID value of the city.

    Returns:
         response:  The JSON representation of the API response
                    containing the data of the city.
    """
    cities = storage.all("City")
    city_key = [key for key in cities.keys()
                if key.split('.')[-1] == city_id]
    if city_key:
        key = city_key[0]
        response = cities.get(key)
        return jsonify(response.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Handler for the HTTP DELETE method for a city by its ID.

    Decorators:
        app_views.route

    Arguments:
        city_id (str):  The unique ID value of the city.

    Returns:
         response:  The JSON representation of the API response
                    an empty dictionary with the status code 200 on success.
    """
    cities = storage.all("City")
    city_key = [key for key in cities.keys()
                if key.split('.')[-1] == city_id]
    if city_key:
        key = city_key[0]
        city = cities.get(key)
        storage.delete(city)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Handler for the HTTP POST method for cities in a state.

    Decorators:
        app_views.route

    Arguments:
        state_id (str):  The unique ID value of the state.

    Returns:
         response: The JSON representation of the API response
                   containing the new City with the status code 201 on success.
    """
    req_body = request.get_json()
    if not req_body:
        abort(400, "Not a JSON")
    if not ('name' in req_body.keys()):
        abort(400, "Missing name")
    states = storage.all('State')
    city_state_key = [key for key in states.keys()
                      if key.split('.')[-1] == state_id]
    if city_state_key:
        city = City(state_id=state_id, **req_body)
        city.save()
        response = city.to_dict()
        return (jsonify(response), 201)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Handler for the HTTP PUT method for a city by its ID.

    Decorators:
        app_views.route

    Arguments:
        city_id (str):  The unique ID value of the city.

    Returns:
         response:  The JSON representation of the API response
                    containing the modified City
                    with the status code 200 on success.
    """
    cities = storage.all("City")
    city_key = [key for key in cities.keys()
                if key.split('.')[-1] == city_id]
    if city_key:
        key = city_key[0]
    else:
        abort(404)
    city = cities.get(key)
    if not city:
        abort(404)
    req_body = request.get_json()
    if not req_body:
        abort(400, "Not a JSON")
    for key, value in req_body.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(city, key, value)
    city.save()
    response = city.to_dict()
    return (jsonify(response), 200)
