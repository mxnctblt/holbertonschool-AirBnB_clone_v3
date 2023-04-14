#!/usr/bin/python3
""" Create a new view for User object that handles
all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from flasgger import swag_from
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users_get_all():
    """ Retrieves the list of all User objects """
    return jsonify([u.to_dict() for u in storage.all("User").values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def users_get(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def users_delete(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def users_create():
    """ Creates a User """
    props = request.get_json()
    if props is None:
        return "Not a JSON", 400
    if props.get("email") is None:
        return "Missing email", 400
    if props.get("password") is None:
        return "Missing password", 400
    new_user = User(**props)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def users_update(user_id):
    """ Updates a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    props = request.get_json()
    if props is None:
        return "Not a JSON", 400
    for key, value in props.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
