#!/usr/bin/python3
"""
App folder
"""

from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    call storage.close
    """
    storage.close()


@app.errorhandler(404)
def error(e):
    """
    404 error handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
