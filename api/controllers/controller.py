"""
Module controlling views
"""
import jwt
import datetime
from flask import request, jsonify
from api.models.user import Users
from api.models.order import Orders
from api.config.config import Security
from api.config.data_validation import DataValidation


class Controller:
    """
    Controller class that dispatches request to different methods
    """

    def __init__(self):
        """
        Class contructor for initialising constructor object
        """
        self.req = request
        self.security_key = Security().key
        self.user = Users()
        self.order = Orders()

    def token_value(self):
        """Method that returns the current token"""
        return (jwt.decode(request.headers['token'], self.security_key))['user']

    def login(self):
        """
        Method for login that deals with params from views
        """
        data = self.req.get_json()
        user_data = self.user.check_credentials(data['username'], data['password'])

        if user_data:
            token = jwt.encode({
                "user": {"user_id": user_data['user_id'], "usertype": user_data['usertype']},
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, self.security_key)
            return jsonify({"status": "success", "message": "you have logged in successfully","token": token.decode('UTF-8')}), 200
        return jsonify({"status": "failure", "error": {"message": "invalid username or password"}}), 401

    def signup(self):
        """
        Method for signup that deals with params from views
        """
        value = DataValidation(self.req).validator(['username', 'firstname', 'lastname', 'contact', 'email', 'password'], 'signup')
        if isinstance(value, bool):
            data = self.req.get_json()
            if not self.user.check_user_details(data['username'], data['email']):
                self.user.add_user(dict(username=data['username'], firstname=data['firstname'], lastname=data['lastname'], contact=data['contact'], email=data['email'], password=data['password'], usertype='user'))
                return jsonify({"status": "success", "message": "you have signed up successfully"}), 200
            return jsonify({"status": "failure", "error": {"message": "username or email already exists"}}), 406
        return value

    def get_users(self):
        """
        Method that returns all users to views
        """
        if (self.token_value())['usertype'] == "admin":
            if self.user.get_all_users():
                return jsonify({"status": "success", "data": self.user.get_all_users()}), 200
            return jsonify({"status": "failure", "error": {"message": "no user found"}}), 404
        return jsonify({"status": "failure", "error": {"message": "only admin can access this resource"}}), 401

    def create_order(self):
        """
        Method for creating a parcel delivery order
        """
        if (self.token_value())['usertype'] == 'user':
            value = DataValidation(self.req).validator(['product', 'description', 'weight', 'pickup', 'destination'], 'order')
            if isinstance(value, bool):
                data = self.req.get_json()
                order = dict(order_id=None, product=data['product'], present=['pickup'], description=data['description'], weight=data['weight'], order_status='pending', pickup=data['pickup'], destination=data['destination'], user_id=(self.token_value())['user_id'], usertype=None)
                resp = self.order.create_order(order)
                if resp:
                    return jsonify({"status": "success", "data": resp}), 201
                return jsonify({"status": "failure", "error": {"message": "you have created that order previously"}}), 400
            return value
        return jsonify({"status": "failure", "error": {"message": "only users can make orders"}}), 401


    def get_order(self, order_id=None):
        """
        Method for getting orders 
        """
        if (self.token_value())['usertype'] == 'admin':
            if order_id is None:
                data = self.order.get_order()
                if data:
                    return jsonify({"status": "success", "data": data}), 200
                return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404

            data = self.order.get_order(order_id)
            if data:
                return jsonify({"status": "success", "data": data}), 200
            return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404

        if (self.token_value())['usertype'] == 'user':

            if order_id is None:
                data = self.order.get_order(None, (self.token_value())['user_id'])
                if data:
                    return jsonify({"status": "success", "data": data}), 200
                return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404

            data = self.order.get_order(order_id, (self.token_value())['user_id'])
            if data:
                return jsonify({"status": "success", "data": data}), 200
            return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404

    def get_order_user(self, user_id):
        """
        Method for getting orders by a specifc user
        """
        if (self.token_value())['usertype'] == 'admin' or ((self.token_value())['usertype'] == 'user' and (self.token_value())['user_id'] == user_id):
            data = self.order.get_order(None, user_id)
            if data:
                return jsonify({"status": "success", "data": data}), 200
            return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404
        return jsonify({"status": "failure", "error": {"message": "you can't access this resource"}}), 401

    def change_product(self, order_id, usertype, details, type):
        """
        Method for changing details of an order
        """
        if (self.token_value())['usertype'] == usertype: 
            value = DataValidation.validate_product_change(self.req, type)
            if isinstance(value, bool):
                data = self.order.get_order(order_id)
                if data:
                    if data['order_status'] == 'cancelled' or data['order_status'] == 'delivered':
                        return jsonify({"status": "failure","error": {"message": "you cannot change details of a delivered or cancelled order"}}), 404
                    user_id = [None if usertype == 'admin' else (self.token_value())['user_id']]
                    req = ['cancelled' if type == 'cancel' else (request.json)['data']]
                    ord = self.order.update_order_details(order_id, req[0], details, user_id[0])
                    return jsonify({"status": "success", "data": ord}), 200
                return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404
            return value
        return jsonify({"status": "failure", "error": {"message": "only "+ usertype +" change destination of an order"}}), 401

