#!/usr/bin/python3
"""handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET', 'POST'], strict_slashes=False)
def users():
    """Retrieves the list of all users objects
    """
    if request.method == 'GET':
        listusers = []
        for user in storage.all("User").values():
            listusers.append(user.to_dict())
        return jsonify(listusers)
    if request.method == 'POST':
        json_user = request.get_json()
        if json_user is None:
            abort(400, "Not a JSON")
        if not json_user.get('name'):
            abort(400, "Missing name")
        user = User(**json_user)
        storage.new(user)
        storage.save()
        storage.reload()
        return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def users_id(user_id):
    """Retrieves a Amenity object
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())
    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        json_user = request.get_json()
        if json_user is None:
            abort(400, "Not a JSON")
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
