"""
Module for testing
"""
from unittest import TestCase
from flask import json
from run import APP
from api.config.database import Database
from api.tests.test_helper.create_order import CreateOrder


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
            '/api/v2/auth/signup',
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
            '/api/v2/auth/login',
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
        post = CreateOrder().create_order('mulago', 'kyebando', 'this is a smartphone', 5, 'iphone', self.token)

        resp = json.loads(post.data)
        self.assertEqual(resp['data']['order_status'], 'pending')
        self.assertEqual(resp['data']['product'], 'iphone')
        self.assertEqual(resp['status'], 'success')
        self.assertEqual(post.status_code, 201)

    def test_get_orders(self):
        """
        Method for testing get orders
        """
        CreateOrder().create_order('mulago', 'kyebando', 'this is a smartphone', 5, 'iphone', self.token)
        CreateOrder().create_order('makindye', 'mutundwe', 'this is a smartphone', 5, 'itel', self.token)
        CreateOrder().create_order('bukoto', 'kamwokya', 'this is a smartphone', 5, 'techno', self.token)

        post = self.client().get(
            '/api/v2/parcels/',
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'success')
        self.assertEqual(len(resp['data']), 3)
        self.assertEqual(post.status_code, 200)

    def test_single_order(self):
        """
        Method for checking single order
        """
        CreateOrder().create_order('mukono', 'namanve', 'this is a smartphone', 5, 'Black Berry', self.token)
        post = self.client().get(
            '/api/v2/parcels/1',
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'success')
        self.assertEqual(resp['data']['product'], 'Black Berry')
        self.assertEqual(post.status_code, 200)

    def test_user_order_fails(self):
        """
        Method for checking failure of user order
        """
        CreateOrder().create_order('arua', 'jinja', 'this is a smartphone', 4, 'Samsung', self.token)
        post = self.client().get(
            '/api/v2/users/4/parcels',
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(resp['error']['message'], "you can't access this resource")
        self.assertEqual(post.status_code, 401)


    def test_cancel_order(self):
        """
        Method for checking cancel order
        """
        CreateOrder().create_order('moroto', 'malaba', 'this is a smartphone', 4, 'Nokia', self.token)

        post = self.client().put(
            '/api/v2/parcels/1/cancel',
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'success')
        self.assertEqual(resp['data']['pickup'], 'moroto')
        self.assertEqual(resp['data']['product'], 'Nokia')
        self.assertEqual(post.status_code, 200)


    def test_change_destination(self):
        """
        Method for checking change destination
        """
        CreateOrder().create_order('yumbe', 'karamoja', 'this is a smartphone', 4, 'LG', self.token)

        post = self.client().put(
            '/api/v2/parcels/1/destination',
            data=json.dumps({"data":"arusha"}),
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'success')
        self.assertEqual(resp['data']['pickup'], 'yumbe')
        self.assertEqual(resp['data']['destination'], 'arusha')
        self.assertEqual(resp['data']['product'], 'LG')
        self.assertEqual(post.status_code, 200)


    def test_change_status_fails(self):
        """
        Method for checking failure of change destination
        """
        CreateOrder().create_order('yumbe', 'karamoja', 'this is a smartphone', 4, 'LG', self.token)

        post = self.client().put(
            '/api/v2/parcels/1/status',
            data=json.dumps({"data":"delivered"}),
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(resp['error']['message'], 'only admin change destination of an order')
        self.assertEqual(post.status_code, 401)


    def test_change_present_location_fails(self):
        """
        Method for checking failure of change destination
        """
        CreateOrder().create_order('yumbe', 'karamoja', 'this is a smartphone', 4, 'LG', self.token)

        post = self.client().put(
            '/api/v2/parcels/1/presentLocation',
            data=json.dumps({"data":"arusha"}),
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(resp['error']['message'], 'only admin change destination of an order')
        self.assertEqual(post.status_code, 401)


    def test_string_error(self):
        """
        Method for checking string errors
        """
        post = self.client().post(
            '/api/v2/parcels',
            data=json.dumps(dict(
                pickup='mulago',
                destination='ntinda',
                description='This is a smart phone',
                weight='dfgd',
                product='iPhone',
            )),
            content_type='application/json',
            headers={'token': self.token}
        )

        resp = json.loads(post.data)
        self.assertEqual(resp['status'], 'failure')
        self.assertEqual(resp['error']['message'], "dfgd should be a integer and greater than 0")
        self.assertEqual(post.status_code, 400)

    def test_int_error(self):
        """
        Method for checking int errors
        """
        post = self.client().post(
            '/api/v2/parcels',
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
        self.assertEqual(resp['error']['message'], "786 should be a string")
        self.assertEqual(post.status_code, 400)

    def test_empty_error(self):
        """
        Method for checking empty errors
        """
        post = self.client().post(
            '/api/v2/parcels',
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

    def test_key_error(self):
        """
        Method for checking key errors
        """
        post = self.client().post(
            '/api/v2/parcels',
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

    def test_content_error(self):
        """
        Method for checking content errors
        """
        post = self.client().post(
            '/api/v2/parcels',
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
        self.assertEqual(post.status_code, 406)
