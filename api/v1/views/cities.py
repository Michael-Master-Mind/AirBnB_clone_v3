#!/usr/bin/python3
"""
module to generate json response
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.city import City


@app_views.route('/cities', strict_slashes=False)
def all_cities():
    """ display all cities """
    response = []
    cities = storage.all(City)
    for city in cities.values():
        response.append(city.to_dict())
    return jsonify(response)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city_by_id(city_id):
    """ display city by id """
    response = storage.get(City, city_id)
    if response is None:
        abort(404)
    return jsonify(response.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id=None):
    """ delete city by id """
    if city_id is None:
        abort(404)
    else:
        trash = storage.get(City, city_id)
        if trash is not None:
            storage.delete(trash)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def create_city():
    """ creates a new city """
    try:
        new = request.get_json()
    except Exception:
        pass
    if new is None or type(new) is not dict:
        abort(400, 'Not a JSON')
    if 'name' not in new.keys():
        abort(400, 'Missing Name')
    response = City(**new)
    response.save()
    return make_response(jsonify(response.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """ update an existing city """
    response = storage.get(City, city_id)
    if city_id is None or response is None:
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
