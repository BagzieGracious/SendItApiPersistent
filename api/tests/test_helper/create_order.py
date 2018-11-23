"""
Module for testing create order
"""
from flask import json
from run import APP


class CreateOrder:
	"""
	Create Order class for creating testing data
	"""

	def __init__(self):
		self.app = APP
		self.client = self.app.test_client

	def create_order(self, pickup, destination, description, weight, product, token):
		"""
		Method for creating orders in the database
		"""
		post = self.client().post(
            '/api/v2/parcels',
            data=json.dumps(dict(
                pickup=pickup,
                destination=destination,
                description=description,
                weight=weight,
                product=product,
            )),
            content_type='application/json',
            headers={'token': token}
        )
		return post