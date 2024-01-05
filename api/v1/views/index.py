#!/usr/bin/python3
from flask import jsonify
from . import app_views

@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    # Retrieve the counts using the count() method from storage
    stats = {
        'objects': {
            'A': storage.count('A'),
            'B': storage.count('B'),
            # Add more object types as needed
        }
    }

    return jsonify(stats)
