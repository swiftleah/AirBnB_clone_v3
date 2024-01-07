#!/usr/bin/python3
""" registers blueprint """
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})
app.register_blueprint(app_views, url_prefix="/api/v1")
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception):
    """handles teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ return error msg `Not Found` """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
