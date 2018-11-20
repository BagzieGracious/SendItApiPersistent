"""
Module to return validations values
"""
from flask import jsonify


class DataValidation:
    """
    Class with methods to return validation values
    """
    error_msg = {"status": 'failure', "error":{"message":""}}

    def __init__(self, req, type):
        """
        Constructor for initializing datavaldation class
        """
        self.req = req
        self.data = self.req.get_json()
        self.type = type

    def err(self, msg):
        """
        Method returns general error message
        """
        DataValidation.error_msg['error']['message'] = msg
        return DataValidation.error_msg

    def string_check(self, lst):
        """
        Method for checking strings criteria
        """
        for error in lst:
            if not isinstance(error, str):
                return jsonify(self.err('username, email, and password should be a string')), 400
        return True

    def validate(self):
        """
        Method for validating inputs
        """
        if self.type == 'user':
            if self.req.content_type == 'application/json':
                key = ['email', 'username', 'password']
                if set(key).issubset(self.data):
                    if isinstance(self.data['email'], str) and isinstance(self.data['username'], str) and isinstance(self.data['password'], str):
                        if self.data['email'] != '' and self.data['username'] != '' and self.data['password'] != '':
                            return True
                        return jsonify(self.err('no field should be empty')), 400
                    return jsonify(self.err('email, username and password should be a string')), 400
                return jsonify(self.err('some field is missing (email, password, username)')), 400
            return jsonify(self.err('only json data is allowed')), 400

        if self.type == 'order':
            if self.req.content_type == 'application/json':
                key = ['pickup', 'destination', 'description', 'weight', 'product']
                if set(key).issubset(self.data):
                    if isinstance(self.data['weight'], int) and self.data['weight'] > 0:
                        if isinstance(self.data['pickup'], str) and isinstance(self.data['description'], str) and isinstance(self.data['destination'], str) and isinstance(self.data['product'], str):
                            if self.data['pickup'] != '' and self.data['description'] != '' and self.data['destination'] and self.data['product'] != '' and self.data['weight'] != '':
                                return True
                            return jsonify(self.err('no field should be empty')), 400
                        return jsonify(self.err('pickup, destination, description, and product should be a string')), 400
                    return jsonify(self.err('weight should be an integer and above 0')), 400
                return jsonify(self.err('some field is missing')), 400
            return jsonify(self.err('only json data is allowed')), 400
