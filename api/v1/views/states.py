#!/usr/bin/python3
""" creates a new view for state objects """
from models import storage
from flask import jsonify, abort, request
from flasgger.utils import swag_from
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """ handles GET req to retrieve state objects """
    allStates = storage.all(State).values()
    return jsonify([state.to_dict() for state in allStates])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ handles GET req to retrieve a specific state by object id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ handles DELETE req to delete specific state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """ handles POST req to create new state object """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    newState = State(**data)
    newState.save()
    return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ handles PUT req to update specific state object by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
