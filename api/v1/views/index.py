#!/usr/bin/python3
"""
index files
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    status route
    return ok with json
    """
    data = {
        "status": "OK"
    }

    ret = jsonify(data)
    ret.status_code = 200

    return ret


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    stats of all objs route
    return all obj in json
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    ret = jsonify(data)
    ret.status_code = 200

    return ret
