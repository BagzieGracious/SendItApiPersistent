"""
Module that acts a model, for handling data manipulation
"""
from flask import jsonify
from api.config.database import Database


class Model:
    """
    model class that add data to data structures
    """

    def get_orders(self):
        """
        method for get data from data structures
        """
        orderList = []
        data = Database().get_all_orders()
        if not data:
            return jsonify({"status": "failure", "error": {"message": "no order found"}}), 404

        for order in data:
            odr = {
                "order_id": order[0],
                "product": order[1],
                "description": order[2],
                "weight": order[3],
                "order_status": order[4],
                "pickup": order[5],
                "destination": order[6],
                "user_id": order[7],
                "order_date": order[8]
            }
            orderList.append(odr)
        return jsonify({"status": "success", "data":orderList}), 200

    def get_single_order(self, order_id, user_id=None):
        if user_id is None:
            order = Database().get_admin_single_order(order_id)
            if order:
                ord = {
                    "order_id": order[0],
                    "product": order[1],
                    "description": order[2],
                    "weight": order[3],
                    "order_status": order[4],
                    "pickup": order[5],
                    "destination": order[6],
                    "user_id": order[7],
                    "order_date": order[8]
                }
                return jsonify({"status": "success", "data": ord}), 200
            return jsonify({"status": "failure", "error": {"message": "order not found"}}), 404

        order = Database().get_user_single_order(order_id, user_id)
        if order:
            ord = {
                "order_id": order[0],
                "product": order[1],
                "description": order[2],
                "weight": order[3],
                "order_status": order[4],
                "pickup": order[5],
                "destination": order[6],
                "user_id": order[7],
                "order_date": order[8]
            }
            return jsonify({"status": "success", "data": ord}), 200
        return jsonify({"status": "failure", "error": {"message": "order not found"}}), 404


    def get_order_user(self, user_id):
        """
        Methods for get data posted by a specific user
        """
        orderList = []
        data = Database().get_order_by_user(user_id)
        if not data:
            return jsonify({"status": "failure", "error": {"message": "order not found"}}), 404

        for order in data:
            ord = {
                "order_id": order[0],
                "product": order[1],
                "description": order[2],
                "weight": order[3],
                "order_status": order[4],
                "pickup": order[5],
                "destination": order[6],
                "user_id": order[7],
                "order_date": order[8]
            }
            orderList.append(ord)
        return jsonify({"status": "success", "data": orderList}), 200


    def cancel_order(self, order_id, user_id):
        """
        Method for cancelling parcel delivery order
        """
        data = Database().check_for_order_change(order_id)
        if not data:
            return jsonify({"status": "failure", "error": {"message": "order not found"}}), 404
        if data[7] == user_id:
            if data[4] == "cancelled" or data[4] == "delivered":
                return jsonify({"status": "failure","error": {"message": "you cannot cancel a delivered or cancelled order"}}), 404
            dt = Database().cancel_order(order_id)
            ord = {
                "order_id": dt[0],
                "product": dt[1],
                "description": dt[2],
                "weight": dt[3],
                "order_status": dt[4],
                "pickup": dt[5],
                "destination": dt[6],
                "user_id": dt[7],
                "order_date": dt[8]
            }
            return jsonify({"status": "success", "data": ord}), 200
        return jsonify({"status": "failure", "error": {"message": "you are not allowed to access this resource"}}), 404

    def change_destination(self, order_id, user_id, destination):
        data = Database().check_for_order_change(order_id)
        if not data:
            return jsonify({"status": "failure", "error": {"message": "order not found"}}), 404
        if data[7] == user_id:
            if data[4] == "cancelled" or data[4] == "delivered":
                return jsonify({"status": "failure", "error": {"message": "you cannot change destination of a delivered or cancelled order"}}), 404
            dt = Database().change_destination(order_id,destination)
            ord = {
                "order_id": dt[0],
                "product": dt[1],
                "description": dt[2],
                "weight": dt[3],
                "order_status": dt[4],
                "pickup": dt[5],
                "destination": dt[6],
                "user_id": dt[7],
                "order_date": dt[8]
            }
            return jsonify({"status": "success", "data": ord}), 200
        return jsonify({"status": "failure", "error": {"message": "you are not allowed to access this resource"}}), 404

    def change_status(self, parcel_id, status):
        data = Database().check_for_order_change(parcel_id)
        if not data:
            return jsonify({"status": "failure", "error": {"message": "order not found"}}), 404
        if data[4] == "cancelled" or data[4] == "delivered":
            return jsonify({"status": "failure", "error": {"message": "you cannot change status of a delivered or cancelled order"}}), 404
        dt = Database().change_status(parcel_id, status)
        ord = {
            "order_id": dt[0],
            "product": dt[1],
            "description": dt[2],
            "weight": dt[3],
            "order_status": dt[4],
            "pickup": dt[5],
            "destination": dt[6],
            "user_id": dt[7],
            "order_date": dt[8]
        }
        return jsonify({"status": "success", "data": ord}), 200



    def create_order(self, order):
        """
        method for add an order in the data structure
        """
        data = Database().add_parcel(order)
        if data:
            order = {
                'order_id': data[0],
                'user_id': data[7],
                'pickup': data[5],
                'destination': data[6],
                'description': data[2],
                'weight': data[4],
                'product': data[1],
                'order_status': data[5],
                'order_date': data[8]
            }
            return jsonify({"status": "success", "data": order}), 201
        return jsonify({"status": "failure", "error": {"message": "you have created that order previously"}}), 400