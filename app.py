#!/usr/bin/python3
"""
This module contains the main application for the AirBnB clone RESTful API.
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    """
    Returns the status of the API.
    """
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

