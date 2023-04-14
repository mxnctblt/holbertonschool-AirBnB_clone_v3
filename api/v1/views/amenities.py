#!/usr/bin/python3
""" Create a new view for Amenity objects that handles
all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from flasgger import swag_from
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """ Retrieves the list of all Amenity objects """
    return jsonify([a.to_dict() for a in storage.all("Amenity").values()])


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_get(amenity_id):
    """ Retrieves a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def amenity_create():
    """ Creates a Amenity """
    props = request.get_json()
    if props is None:
        return "Not a JSON", 400
    if props.get("name") is None:
        return "Missing name", 400
    new_amenity = Amenity(**props)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def amenity_update(amenity_id):
    """ Updates a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    props = request.get_json()
    if type(props) != dict:
        abort(400, description="Not a JSON")
    for key, value in props.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
