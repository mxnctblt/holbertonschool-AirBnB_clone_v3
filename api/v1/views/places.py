#!/usr/bin/python3
""" Create a new view for Place objects that handles
all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from flasgger import swag_from
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([p.to_dict() for p in city.places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def places_get(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def places_delete(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def places_create(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    props = request.get_json()
    if props is None:
        return "Not a JSON", 400
    if props.get("user_id") is None:
        return "Missing user_id", 400
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if props.get("name") is None:
        return "Missing name", 400
    props["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def users_update(place_id):
    """ Updates a Place object """
    place = place.get(Place, place_id)
    if place is None:
        abort(404)
    props = request.get_json()
    if props is None:
        return "Not a JSON", 400
    for key, value in props.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
