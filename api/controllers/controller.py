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


class UserController:
    """
    Controller class that inherits MethodView object
    """

    def __init__(self):
        """
        Class contructor for initialising model object
        """
        self.req = request
        self.security_key = Security().key
        self.user = Users()

    def to_dict(self, *args):
        return {
            "username": args[0],
            "firstname": args[1],
            "lastname": args[2],
            "contact": args[3],
            "email": args[4],
            "password": args[5],
            "user_id": args[6],
            "usertype": args[7]
        }

    def token_value(self):
        return (jwt.decode(request.headers['token'], self.security_key))['user']

    def login(self):
        """
        Method for login that deals with params from views
        """
        data = self.req.get_json()
        user_data = self.user.check_credentials(data['username'], data['password'])

        if user_data:
            token = jwt.encode({
                "user": {"user_id": user_data[0], "usertype": user_data[7]},
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, self.security_key)
            return jsonify({"status": "success", "message": "you have logged in successfully","token": token.decode('UTF-8')}), 200
        return jsonify({"status": "failure", "error": {"message": "invalid username or password"}}), 401

    def signup(self):
        """
        Method for signup that deals with params from views
        """
        value = DataValidation(self.req, 'user').validate()
        if isinstance(value, bool):
            data = self.req.get_json()
            if not self.user.check_user_details(data['username'], data['email']):
                user_data = self.to_dict(data['username'], data['firstname'], data['lastname'], data['contact'], data['email'], data['password'], None, 'user')
                self.user.add_user(user_data)
                return jsonify({"status": "success", "message": "you have signed up successfully"}), 200
            return jsonify({"status": "failure", "error": {"message": "username or email already exists"}}), 403
        return value

    def get_users(self):
        """
        Method that returns all users to views
        """
        if (self.token_value())['usertype'] == "admin":
            if self.user.get_all_users():
                user_list = []
                for usr in self.user.get_all_users():
                    user = self.to_dict(usr[1], usr[2], usr[3], usr[4], usr[5], usr[6], usr[0], usr[7])
                    user_list.append(user)
                return jsonify({"status": "success", "data": user_list}), 200
            return jsonify({"status": "failure", "error": {"message": "no user found"}}), 404
        return jsonify({"status": "failure", "error": {"message": "only admin can access this resource"}}), 401


class OrderController:

    def __init__(self):
        self.req = request
        self.security_key = Security().key
        self.order = Orders()

    def token_value(self):
        return (jwt.decode(request.headers['token'], self.security_key))['user']

    def to_dict(self, *args):
        return {
            "order_id": args[0],
            "product": args[1],
            "description": args[2],
            "weight": args[3],
            "order_status": args[4],
            "pickup": args[5],
            "destination": args[6],
            "user_id": args[7],
            "order_date": args[8],
        }

    def create_order(self):
        """
        Method for creating a parcel delivery order
        """
        if (self.token_value())['usertype'] == 'user':
            value = DataValidation(self.req, 'order').validate()
            if isinstance(value, bool):
                data = self.req.get_json()
                order = self.to_dict(None, data['product'], data['description'], data['weight'], 'pending', data['pickup'], data['destination'], (self.token_value())['user_id'], None)
                resp = self.order.create_order(order)

                if resp:
                    resp_data = self.to_dict(resp[0], resp[1], resp[2], resp[3], resp[4], resp[5], resp[6], resp[7], resp[8])
                    return jsonify({"status": "success", "data": resp_data}), 201
                return jsonify({"status": "failure", "error": {"message": "you have created that order previously"}}), 400
            return value
        return jsonify({"status": "failure", "error": {"message": "only users can make orders"}}), 401

    def get_order(self, order_id=None):
        """
        Method for getting orders from datastructures
        """
        if (self.token_value())['usertype'] == 'admin':
            if order_id is None:
                data = self.order.get_order()
                if data:
                    order_list = []
                    for ord in data:
                        order = self.to_dict(ord[0], ord[1], ord[2], ord[3], ord[4], ord[5], ord[6], ord[7], ord[8])
                        order_list.append(order)
                    return jsonify({"status": "success", "data": order_list}), 200
                return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404

            data = self.order.get_order(order_id)
            if data:
                order = self.to_dict(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
                return jsonify({"status": "success", "data": order}), 200
            return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404

        if (self.token_value())['usertype'] == 'user':

            if order_id is None:
                data = self.order.get_order(None, (self.token_value())['user_id'])
                if data:
                    order_list = []
                    for ord in data:
                        order = self.to_dict(ord[0], ord[1], ord[2], ord[3], ord[4], ord[5], ord[6], ord[7], ord[8])
                        order_list.append(order)
                    return jsonify({"status": "success", "data": order_list}), 200
                return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404

            data = self.order.get_order(order_id, (self.token_value())['user_id'])
            if data:
                order = self.to_dict(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
                return jsonify({"status": "success", "data": order}), 200
            return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404

    def get_order_user(self, user_id):
        """
        Method for getting orders by a specifc user
        """
        if (self.token_value())['usertype'] == 'admin' or ((self.token_value())['usertype'] == 'user' and (self.token_value())['user_id'] == user_id):
            data = self.order.get_order(None, user_id)
            if data:
                order_list = []
                for ord in data:
                    order = self.to_dict(ord[0], ord[1], ord[2], ord[3], ord[4], ord[5], ord[6], ord[7], ord[8])
                    order_list.append(order)
                return jsonify({"status": "success", "data": order_list}), 200
            return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404
        return jsonify({"status": "failure", "error": {"message": "you can't access this resource"}}), 401

    def cancel_parcel(self, order_id):
        if (self.token_value())['usertype'] == 'user':
            data = self.order.get_order(order_id, (self.token_value())['user_id'])
            if data:
                if data[4] == 'cancelled' or data[4] == 'delivered':
                    return jsonify({"status": "failure", "error": {"message": "you cannot cancel a delivered or cancelled order"}}), 404

                data = self.order.update_order_details(order_id, 'cancelled', 'order_status')
                order = self.to_dict(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
                return jsonify({"status": "success", "data": order}), 200
            return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404
        return jsonify({"status": "failure", "error": {"message": "only user cancel an order"}}), 404

    def change_destination(self, order_id):
        if (self.token_value())['usertype'] == 'user':
            data = self.order.get_order(order_id, (self.token_value())['user_id'])
            if data:
                if data[4] == 'cancelled' or data[4] == 'delivered':
                    return jsonify({"status": "failure","error": {"message": "you cannot change destination of a delivered or cancelled order"}}), 404

                dest = (request.json)['destination']
                data = self.order.update_order_details(order_id, dest, 'destination')
                order = self.to_dict(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
                return jsonify({"status": "success", "data": order}), 200
            return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404
        return jsonify({"status": "failure", "error": {"message": "only user change destination of an order"}}), 404

    def change_status(self, order_id):
        if (self.token_value())['usertype'] == 'admin':
            data = self.order.get_order(order_id, (self.token_value())['user_id'])
            if data:
                if data[4] == 'cancelled' or data[4] == 'delivered':
                    return jsonify({"status": "failure","error": {"message": "you cannot change status of a delivered or cancelled order"}}), 404

                stat = (request.json)['status']
                data = self.order.update_order_details(order_id, stat, 'order_status')
                order = self.to_dict(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
                return jsonify({"status": "success", "data": order}), 200
            return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404
        return jsonify({"status": "failure", "error": {"message": "only admin change status of an order"}}), 404