#!/usr/bin/python3
"""
index files
"""
from flask import jsonify
from api.v1.views import app_views


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
