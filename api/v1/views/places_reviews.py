#!/usr/bin/python3
""" Create a new view for Review objects that handles
all default RESTFul API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def review_by_place(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_get(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_create(place_id):
    """ Creates a Review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    props = request.get_json()
    if props is None:
        abort(400, "Not a JSON")
    user_id = props.get("user_id")
    if "user_id" not in props:
        abort(400, "Missing user_id")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    text = props.get("text")
    if "text" not in props:
        abort(400, "Missing text")
    props['place_id'] = place_id
    new_review = Review(**props)
    new_review.save()
    return (jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_update(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    props = request.get_json()
    if props is None:
        return "Not a JSON", 400
    for key, value in props.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
