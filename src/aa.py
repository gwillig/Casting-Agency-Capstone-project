from __future__ import absolute_import
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc

from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    CORS(app)

    @app.route('/')
    def index():
        print("hello world")
        return "Welcome to the FAKE Casting Agency"

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)