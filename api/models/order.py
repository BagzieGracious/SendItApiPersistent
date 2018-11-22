"""
Module for handling order business logic
"""
from api.config.database import Database


class Orders:
    """
    Order class that handles business logic for orders
    """
    def __init__(self):
        self.connect = Database().connect
        self.cursor = Database().cursor

    def get_order(self, order_id=None, user_id=None):
        """
        method that retrieves orders from the order table
        """
        if user_id is None:
            if order_id is None:
                sql = "SELECT * FROM orders"
                self.cursor.execute(sql)
                return self.cursor.fetchall()

            sql = "SELECT * FROM orders WHERE order_id = '{}'".format(order_id)
            self.cursor.execute(sql)
            return self.cursor.fetchone()

        if order_id is None:
            sql = "SELECT * FROM orders WHERE user_id = '{}'".format(user_id)
            self.cursor.execute(sql)
            return self.cursor.fetchall()

        sql = "SELECT * FROM orders WHERE user_id = '{}' AND order_id = '{}'".format(user_id, order_id)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def update_order_details(self, order_id, status, type, user_id):
        """
        Method that updates order details in the order table
        """
        if user_id is None:
            sql = "UPDATE orders SET {} = '{}' WHERE order_id = '{}'".format(type, status, order_id)
        else:
            sql = "UPDATE orders SET {} = '{}' WHERE order_id = '{}' AND user_id = '{}'".format(type, status, order_id, user_id)

        self.cursor.execute(sql)
        self.connect.commit()
        sql1 = "SELECT * FROM orders WHERE order_id = %s"
        self.cursor.execute(sql1, [order_id])
        return self.cursor.fetchone()

    def create_order(self, data):
        """
        method that adds an order in the order table
        """
        sql = "SELECT * FROM orders WHERE user_id = %s AND product = %s AND destination = %s"
        self.cursor.execute(sql, [data['user_id'], data['product'], data['destination']])

        if not self.cursor.fetchone():
            sql1 = "INSERT INTO orders( product, description, weight, order_status, pickup, destination, present, user_id)" \
                   " VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql1, [data['product'], data['description'], data['weight'], data['order_status'],
                                       data['pickup'], data['destination'], data['pickup'], data['user_id']])
            self.connect.commit()

            sql = "SELECT * FROM orders WHERE user_id = %s AND product = %s AND destination = %s"
            self.cursor.execute(sql, [data['user_id'], data['product'], data['destination']])
            return self.cursor.fetchone()
        return False
