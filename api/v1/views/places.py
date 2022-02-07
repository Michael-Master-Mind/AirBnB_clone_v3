#!/usr/bin/python3
"""
module to generate json response
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.place import Place


@app_views.route('/places', strict_slashes=False)
def all_places():
    """ display all places """
    response = []
    places = storage.all(Place)
    for place in places.values():
        response.append(place.to_dict())
    return jsonify(response)


@app_views.route('/places/<place_id>', strict_slashes=False)
def place_by_id(place_id):
    """ display place by id """
    response = storage.get(Place, place_id)
    if response is None:
        abort(404)
    return jsonify(response.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id=None):
    """ delete place by id """
    if place_id is None:
        abort(404)
    else:
        trash = storage.get(Place, place_id)
        if trash is not None:
            storage.delete(trash)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/places', methods=['POST'], strict_slashes=False)
def create_place():
    """ creates a new place """
    try:
        new = request.get_json()
    except Exception:
        pass
    if new is None or type(new) is not dict:
        abort(400, 'Not a JSON')
    if 'name' not in new.keys():
        abort(400, 'Missing Name')
    response = Place(**new)
    response.save()
    return make_response(jsonify(response.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """ update an existing place """
    response = storage.get(Place, place_id)
    if place_id is None or response is None:
        abort(404)
    try:
        new = request.get_json()
    except Exception:
        pass
    if new is None or type(new) is not dict:
        abort(400, 'Not a JSON')
    for key in new.keys():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(response, key, new[key])
    response.save()
    return make_response(jsonify(response.to_dict()), 200)
