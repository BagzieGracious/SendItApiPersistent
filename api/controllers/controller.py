"""
Module controlling views
"""
from flask import request, jsonify
import jwt
from api.models.user import Users
from api.models.model import Model
from api.config.data_validation import DataValidation


class Controller:
    """
    Controller class that inherits MethodView object
    """

    def __init__(self):
        """
        Class contructor for initialising model object
        """
        self.req = request
        self.security_key = 'json_web_token'
        self.model = Model()

    def login(self):
        """
        Method for login that deals with params from views
        """
        data = self.req.get_json()
        return Users.check_credentials(data['username'], data['password'])

    def signup(self):
        """
        Method for signup that deals with params from views
        """
        value = DataValidation(self.req, 'user').validate()
        if isinstance(value, bool):
            data = self.req.get_json()
            user = Users(data['username'], data['firstname'], data['lastname'], data['contact'], data['email'], data['password'], 'user')
            return user.add_user()
        return value

    def get_users(self):
        """
        Method that returns all users to views
        """
        token = jwt.decode(request.headers['token'], 'json_web_token')
        if token['user']['usertype'] == "admin":
            return Users.get_all_users()
        return jsonify({"status": "failure", "error": {"message": "only admin can access this resource"}}), 401

    def create_order(self):
        """
        Method for creating a parcel delivery order
        """
        token = jwt.decode(request.headers['token'], 'json_web_token')
        if token['user']['usertype'] == 'user':
            value = DataValidation(self.req, 'order').validate()
            if isinstance(value, bool):
                order_data = self.req.get_json()
                order = {
                    'user_id': token['user']['user_id'],
                    'pickup': order_data['pickup'],
                    'destination': order_data['destination'],
                    'description': order_data['description'],
                    'weight': order_data['weight'],
                    'product': order_data['product'],
                    'status': 'pending'
                }
                return self.model.create_order(order)
            return value
        return jsonify({"status": "failure", "error": {"message": "only users can make orders"}}), 401

    def get_order(self):
        """
        Method for getting orders from datastructures
        """
        token = jwt.decode(request.headers['token'], 'json_web_token')
        if token['user']['usertype'] == 'admin':
            return self.model.get_orders()
        return jsonify({"status": "failure", "error": {"message": "only admin can access this resource"}}), 401

    def get_single_order(self, parcel_id):
        token = jwt.decode(request.headers['token'], 'json_web_token')
        if token['user']['usertype'] == "admin":
            return self.model.get_single_order(parcel_id)
        return self.model.get_single_order(parcel_id, token['user']['user_id'])

    def get_order_user(self, user_id):
        """
        Method for getting orders by a specifc user
        """
        token = jwt.decode(request.headers['token'], 'json_web_token')
        if token['user']['usertype'] == "admin":
            return self.model.get_order_user(user_id)
        if token['user']['user_id'] == user_id:
            return self.model.get_order_user(user_id)
        return jsonify({"status": "failure", "error": {"message": "you can't access this resource"}}), 401

    def cancel_order(self, parcel_id):
        """
        Method for canceling an order
        """
        token = jwt.decode(request.headers['token'], 'json_web_token')
        if token['user']['usertype'] == "user":
            return self.model.cancel_order(parcel_id, token['user']['user_id'])
        return jsonify({"status": "failure", "error": {"message": "only users can cancel an order"}}), 401

    def change_destination(self, parcel_id):
        token = jwt.decode(request.headers['token'], 'json_web_token')
        if token['user']['usertype'] == "user":
            return self.model.change_destination(parcel_id, token['user']['user_id'], request.json['destination'])
        return jsonify({"status": "failure", "error": {"message": "only users can change destination of an order"}}), 401

    def change_status(self, parcel_id):
        token = jwt.decode(request.headers['token'], 'json_web_token')
        if token['user']['usertype'] == "admin":
            if request.json['status'] == "in-transit" or request.json['status'] == "delivered":
                return self.model.change_status(parcel_id, request.json['status'])
            return jsonify({"status": "failure", "error": {"message": "only in-transit or delivered are allowed"}}), 401
        return jsonify({"status": "failure", "error": {"message": "only admin can change status of an order"}}), 401
