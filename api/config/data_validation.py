"""
Module to return validations values
"""
from flask import jsonify
import re
from validate_email import validate_email


class DataValidation:
    """
    Class with methods to return validation values
    """
    error_msg = {"status": 'failure', "error":{"message":""}}

    def __init__(self, req):
        """
        Constructor for initializing datavaldation class
        """
        self.req = req
        self.data = self.req.get_json()

    def err(self, msg):
        """
        Method returns general error message
        """
        DataValidation.error_msg['error']['message'] = msg
        return DataValidation.error_msg

    def type_check(self, lst, type):
        """
        Method that checks if each value in a list of a certain type
        """
        for error in lst:
            if not isinstance(error, type):
                return jsonify(self.err("you have a {} error check your inputs".format(type))), 400
        return True

    def empty_check(self, lst):
        """
        Mehtod that checks if each element is in a list is empty
        """
        for error in lst:
            if error == '':
                return jsonify(self.err("no empty field allowed")), 400
        return True

    def email_check(self, email):
        """
        Method that checks if the email is valid
        """
        if validate_email(email):
            return True
        return jsonify(self.err("invalid email")), 406

    def password_check(self, password):
        """
        Method that checks if the password is greater than 5 chars
        """
        if len(password) >= 6:
            return True
        return jsonify(self.err("password should be greater that 5 chars")), 406

    def contact_check(self, contact):
        """
        Method that checks if the contact is correct
        """
        rgx = re.compile("^[0-9]{10,13}$")
        if rgx.search(contact):
            return True
        return jsonify(self.err("Invalid contact format")), 406

    def validator(self, lst, type):
        """
        Method that validates the request object
        """
        if self.req.content_type == 'application/json':
            if set(lst).issubset(self.data):
                if type == 'signup':
                    err = [
                        self.type_check([self.data['username'], self.data['firstname'], self.data['contact'], self.data['email'], self.data['password']], str), 
                        self.empty_check([self.data['username'], self.data['firstname'], self.data['contact'], self.data['email'], self.data['password']]), 
                        self.email_check(self.data['email']), 
                        self.password_check(self.data['password']),
                        self.contact_check(self.data['contact'])
                    ]

                if type == 'order':
                    err = [
                        self.type_check([self.data['product'], self.data['description'], self.data['pickup'], self.data['destination']], str),
                        self.type_check([self.data['weight']], int),
                        self.empty_check([self.data['product'], self.data['description'], self.data['pickup'], self.data['destination'], self.data['weight']])
                    ]

                for value in err:
                    if not isinstance(value, bool):
                        return value
                return True
            return jsonify(self.err("some field is missing")), 400
        return jsonify(self.err('only json data is allowed')), 406

    @staticmethod
    def validate_product_change(req, type):
        """
        Method that validates the update of products details
        """
        if req.content_type == 'application/json':
            if type == 'cancel':
                return True

            data = req.get_json()
            if set(['data']).issubset(data):
                if type == 'status':
                    if data['data'] == 'in-transit' or data['data'] == 'delivered':
                        return True
                    return jsonify({"status": 'failure', "error":{"message":"only in-transit or delivered status is allowed"}}), 400
                return True
            return jsonify({"status": 'failure', "error":{"message":"some field is missing"}}), 400
        return jsonify({"status": 'failure', "error":{"message":"only json data is allowed"}}), 400