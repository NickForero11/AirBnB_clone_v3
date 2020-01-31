#!/usr/bin/python3
"""Module to handle all the default RestFul API actions for state objects.
"""
from api.v1.views import app_views
from flask import (jsonify, request, abort)
from models import storage
from models.state import State


@app_views.route('/states/<state_id>/states', methods=['GET'],
                 strict_slashes=False)
def states(state_id):
    """Handler for the HTTP GET method for states in a state.
    Decorators:
        app_views.route
    Argument
        state_id (str):  The unique ID value of the state.
    Returns:
         response:  The JSON representation of the API response
                    containing the states in the specificated state.
    """
    states = storage.all("State")
    state_state_key = [key for key in states.keys()
                      if key.split('.')[-1] == state_id]
    if state_state_key:
        key = state_state_key[0]
        list_states = states.get(key).states
        response = [state.to_dict() for state in list_states]
        return jsonify(response)
    abort(404)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Handler for the HTTP GET method for a state by its ID.
    Decorators:
        app_views.route
    Arguments:
        state_id (str):  The unique ID value of the state.
    Returns:
         response:  The JSON representation of the API response
                    containing the data of the state.
    """
    states = storage.all("state")
    state_key = [key for key in states.keys()
                if key.split('.')[-1] == state_id]
    if state_key:
        key = state_key[0]
        response = states.get(key)
        return jsonify(response.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Handler for the HTTP DELETE method for a state by its ID.
    Decorators:
        app_views.route
    Arguments:
        state_id (str):  The unique ID value of the state.
    Returns:
         response:  The JSON representation of the API response
                    an empty dictionary with the status code 200 on success.
    """
    states = storage.all("state")
    state_key = [key for key in states.keys()
                if key.split('.')[-1] == state_id]
    if state_key:
        key = state_key[0]
        state = states.get(key)
        storage.delete(state)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/states', methods=['POST'],
                 strict_slashes=False)
def post_state(state_id):
    """Handler for the HTTP POST method for states in a state.
    Decorators:
        app_views.route
    Arguments:
        state_id (str):  The unique ID value of the state.
    Returns:
         response: The JSON representation of the API response
                   containing the new state with the status code 201 on success.
    """
    req_body = request.get_json()
    if not req_body:
        abort(400, "Not a JSON")
    if not ('name' in req_body.keys()):
        abort(400, "Missing name")
    states = storage.all('State')
    state_state_key = [key for key in states.keys()
                      if key.split('.')[-1] == state_id]
    if state_state_key:
        state = state(state_id=state_id, **req_body)
        state.save()
        response = state.to_dict()
        return (jsonify(response), 201)
    abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Handler for the HTTP PUT method for a state by its ID.
    Decorators:
        app_views.route
    Arguments:
        state_id (str):  The unique ID value of the state.
    Returns:
         response:  The JSON representation of the API response
                    containing the modified state
                    with the status code 200 on success.
    """
    states = storage.all("state")
    state_key = [key for key in states.keys()
                if key.split('.')[-1] == state_id]
    if state_key:
        key = state_key[0]
    else:
        abort(404)
    state = states.get(key)
    if not state:
        abort(404)
    req_body = request.get_json()
    if not req_body:
        abort(400, "Not a JSON")
    for key, value in req_body.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
    state.save()
    response = state.to_dict()
    return (jsonify(response), 200)
