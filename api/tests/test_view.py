"""
Module for testing create order
"""
from unittest import TestCase
from flask import json
from run import APP
from api.config.database import Database


class TestView(TestCase):

    """
    Class that inherits TestCase for testing TDD
    """
    def setUp(self):
        """
        class constructor for initiating flask object
        """
        self.db = Database().clear_tables()
        self.app = APP
        self.client = self.app.test_client
        self.client().post(
            '/api/v1/auth/signup',
            data=json.dumps(dict(
                username='bagzie',
                firstname='bagenda',
                lastname='deogracious',
                contact='0700558588',
                email='bagenda@gmail.com',
                password='bagenda'
            )),
            content_type='application/json'
        )

        login = self.client().post(
            '/api/v1/auth/login',
            data=json.dumps(dict(
                username='bagzie',
                password='bagenda'
            )),
            content_type='application/json'
        )

        login_res = json.loads(login.data)
        self.token = login_res['token']

    def test_create_order(self):
        """
        Method returns create order results
        """
        post = self.client().post(
            '/api/v1/parcels',
            data=json.dumps(dict(
                pickup='mulago',
                destination='ntinda',
                description='This is a smart phone',
                weight=3,
                product='iPhone',
            )),
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['data']['order_status'], 'pending')
        self.assertEqual(resp['status'], 'success')
        self.assertEqual(post.status_code, 201)

    def test_string_error(self):
        """
        Method for checking string errors
        """
        post = self.client().post(
            '/api/v1/parcels',
            data=json.dumps(dict(
                pickup='mulago',
                destination='ntinda',
                description='This is a smart phone',
                weight='',
                product='iPhone',
            )),
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(resp['error']['message'], "you have a <class 'int'> error check your inputs")
        self.assertEqual(post.status_code, 400)

    def test_int_error(self):
        """
        Method for checking int errors
        """
        post = self.client().post(
            '/api/v1/parcels',
            data=json.dumps(dict(
                pickup='mulago',
                destination='ntinda',
                description='This is a smart phone',
                weight=6,
                product=786,
            )),
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(resp['error']['message'], "you have a <class 'str'> error check your inputs")
        self.assertEqual(post.status_code, 400)

    def test_empty_error(self):
        """
        Method for checking empty errors
        """
        post = self.client().post(
            '/api/v1/parcels',
            data=json.dumps(dict(
                pickup='mulago',
                destination='',
                description='This is a smart phone',
                weight=6,
                product='itel',
            )),
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(resp['error']['message'], 'no empty field allowed')
        self.assertEqual(post.status_code, 400)

    """
    def test_key_error(self):
        Method for checking key errors
        post = self.client().post(
            '/api/v1/parcels',
            data=json.dumps(dict(
                pickup='mulago',
                destination='',
                description='This is a smart phone',
                weight=6,
            )),
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(resp['error']['message'], 'some field is missing')
        self.assertEqual(post.status_code, 400)
    """

    def test_content_error(self):
        """
        Method for checking content errors
        """
        post = self.client().post(
            '/api/v1/parcels',
            data=json.dumps(dict(
                pickup='mulago',
                destination='',
                description='This is a smart phone',
                weight=6,
            )),
            content_type='application/javascript',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(resp['error']['message'], 'only json data is allowed')
        self.assertEqual(post.status_code, 400)

    """
    def test_get_orders(self):
        Method for checking get orders
        post = self.client().get(
            '/api/v1/parcels',
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'success')
        self.assertEqual(post.status_code, 200)
    """

    def test_single_order(self):
        """
        Method for checking single errors
        """
        post = self.client().get(
            '/api/v1/parcels/1',
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(post.status_code, 404)

    def test_user_order(self):
        """
        Method for checking user order
        """
        post = self.client().get(
            '/api/v1/users/1/parcels',
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(post.status_code, 404)

    def test_cancel_order(self):
        """
        Method for checking cancel order
        """
        post = self.client().put(
            '/api/v1/parcels/1/cancel',
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(post.status_code, 404)
