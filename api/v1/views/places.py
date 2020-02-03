#!/usr/bin/python3
"""handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """Retrieves the list of all places objects
    """
    placesget = storage.get("City", city_id)

    if placesget is None:
        abort(404)

    if request.method == 'GET':
        listplaces = []
        for place in placesget.places:
            listplaces.append(place.to_dict())
        return jsonify(listplaces)

    if request.method == 'POST':
        json_place = request.get_json()
        if json_place is None:
            abort(400, "Not a JSON")
        if not json_place.get('name'):
            abort(400, "Missing name")
        if not json_place.get('user_id'):
            abort(400, "Missing user_id")
        userget = storage.get("User", json_place.get("user_id"))
        if userget is None:
            abort(404)
        json_place["city_id"] = city_id
        json_place["user_id"] = json_place.get("user_id")
        place = Place(**json_place)
        storage.new(place)
        storage.save()
        storage.reload()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def places_id(place_id):
    """Retrieves a place object
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        json_place = request.get_json()
        if json_place is None:
            abort(400, "Not a JSON")
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at', 'user_id',
                           'city_id']:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
