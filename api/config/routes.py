"""
Module for rendering routes
"""
import jwt
from functools import wraps
from flask import request, jsonify
from api.config.config import Security
from api.controllers.controller import Controller


class Routes:
    """
    Create a Routes class
    """
    def __init__(self):
        self.controller = Controller()

    def fetch_routes(self, app):
        """
        static method for fetching all routes
        """

        def required(func):
            @wraps(func)
            def decorated(*args, **kwargs):
                if 'token' in request.headers:
                    token = request.headers['token']
                else:
                    return jsonify({"status": "failure", "error": {"message": "Login, in-order to access this view"}}), 400
                try:
                    jwt.decode(token, Security().key)
                except:
                    return jsonify({"status": "failure", "error": {"message": "Invalid, token"}}), 400
                return func(*args, **kwargs)
            return decorated

        @app.route('/')
        def index():
            return "<h1>Welcome to send-it</h1> <p>the only place that you can feel safe with delivery orders</p>"

        @app.route('/api/v1/auth/login', methods=['POST'], strict_slashes=False)
        def login():
                return self.controller.login()

        @app.route('/api/v1/auth/signup', methods=['POST'], strict_slashes=False)
        def signup():
            return self.controller.signup()

        @app.route('/api/v1/users', methods=['GET'], strict_slashes=False)
        @required
        def get_users():
            return self.controller.get_users()
            
        @app.route('/api/v1/parcels', methods=['POST', 'GET'], strict_slashes=False)
        @required
        def parcels():
            if request.method == 'POST':
                return self.controller.create_order()
            return self.controller.get_order()

        @app.route('/api/v1/parcels/<int:parcel_id>', methods=['GET'], strict_slashes=False)
        @required
        def get_single_parcel(parcel_id):
            return self.controller.get_order(parcel_id)

        @app.route('/api/v1/users/<int:user_id>/parcels', methods=['GET'], strict_slashes=False)
        @required
        def get_parcel_user(user_id):
            return self.controller.get_order_user(user_id)

        @app.route('/api/v1/parcels/<int:parcel_id>/cancel', methods=['PUT'], strict_slashes=False)
        @required
        def cancel_parcel(parcel_id):
            return self.controller.change_product(parcel_id, 'user', 'order_status', 'cancel')

        @app.route('/api/v1/parcels/<int:parcel_id>/destination', methods=['PUT'], strict_slashes=False)
        @required
        def change_parcel_destination(parcel_id):
            return self.controller.change_product(parcel_id, 'user', 'order_status', 'destination')

        @app.route('/api/v1/parcels/<int:parcel_id>/status', methods=['PUT'], strict_slashes=False)
        @required
        def change_status(parcel_id):
            return self.controller.change_product(parcel_id, 'admin', 'order_status', 'status')

        @app.route('/api/v1/parcels/<int:parcel_id>/presentLocation', methods=['PUT'], strict_slashes=False)
        @required
        def change_location(parcel_id):
            return self.controller.change_product(parcel_id, 'admin', 'present', 'present')
