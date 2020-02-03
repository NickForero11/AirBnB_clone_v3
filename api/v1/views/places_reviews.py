#!/usr/bin/python3
"""handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews(place_id):
    """Retrieves the list of all reviews objects
    """
    reviewget = storage.get("Place", place_id)

    if reviewget is None:
        abort(404)

    if request.method == 'GET':
        listreviews = []
        for review in reviewget.reviews:
            listreviews.append(review.to_dict())
        return jsonify(listreviews)

    if request.method == 'POST':
        json_review = request.get_json()
        if json_review is None:
            abort(400, "Not a JSON")
        if not json_review.get('user_id'):
            abort(400, "Missing user_id")
        userget = storage.get("User", json_review.get("user_id"))
        if userget is None:
            abort(404)
        if not json_review.get("text"):
            abort(400, "Missing text")
        json_review["city_id"] = json_review.get(" city_id")
        json_review["user_id"] = json_review.get("user_id")
        review = Place(**json_review)
        storage.new(review)
        storage.save()
        storage.reload()
        return jsonify(review.to_dict()), 201


@app_views.route("reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def reviews_id(review_id):
    """Retrieves a place object
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        json_place = request.get_json()
        if json_place is None:
            abort(400, "Not a JSON")
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at', 'user_id',
                           'place_id']:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
