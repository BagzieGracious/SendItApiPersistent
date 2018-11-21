"""
Module to return validations values
"""
from validate_email import validate_email
from flask import jsonify


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
        self.type = type

    def err(self, msg):
        """
        Method returns general error message
        """
        DataValidation.error_msg['error']['message'] = msg
        return DataValidation.error_msg

    def type_check(self, lst, type):
        for error in lst:
            if not isinstance(error, type):
                return jsonify(self.err("you have a {} error check your inputs".format(type))), 400
        return True

    def empty_check(self, lst):
        for error in lst:
            if error == '':
                return jsonify(self.err("no empty field allowed")), 400
        return True

    def email_check(self, email):
        if validate_email(email):
            return True
        return jsonify(self.err("invalid email"))

    def password_check(self, password):
        if len(password) >= 6:
            return True
        return jsonify(self.err("password should be greater that 5 chars"))

    def key_check(self, lst, request):
        if set(lst).issubset(request):
            return True
        return jsonify(self.err('some field is missing')), 400

    def validator(self, lst, type):
        if self.req.content_type == 'application/json':
            if self.key_check(lst, self.data):
                if type == 'signup':
                    err = [
                        self.type_check([self.data['username'], self.data['firstname'], self.data['contact'], self.data['email'], self.data['password']], str), 
                        self.empty_check([self.data['username'], self.data['firstname'], self.data['contact'], self.data['email'], self.data['password']]), 
                        self.email_check(self.data['email']), 
                        self.password_check(self.data['password'])
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
            return key_check(lst, self.data)
        return jsonify(self.err('only json data is allowed')), 400   
        
