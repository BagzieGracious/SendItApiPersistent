import jwt
import datetime
from flask import jsonify
from api.config.database import Database


class Users:
    userLst = []

    def __init__(self, *args):
        self.user = args[0]
        self.first = args[1]
        self.last = args[2]
        self.cont = args[3]
        self.email = args[4]
        self.pswd = args[5]
        self.type = args[6]
        self.database = Database().create_users_table()

    def add_user(self):
        """
        Method for adding a user to data structures
        """
        if Database().check_user_exists(self.user, self.email):
            return jsonify({"status": "failure", "error": {"message": "user already exists"}}), 409
        Database().add_user(self.user, self.first, self.last, self.last, self.email, self.pswd, self.type)
        return jsonify({"status": "success", "message": "you have signed up successfully"}), 200

    @staticmethod
    def check_credentials(username, password):
        """
        Method for checking users username or password
        """
        if Database().authorize_user(username, password):
            data = Database().user_data_username(username)
            token = jwt.encode({
                "user": {"user_id": data[0], "usertype": data[7]},
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, 'json_web_token')
            return jsonify({"status": "success", "message": "you have logged in successfully", "token": token.decode('UTF-8')}), 200
        return jsonify({"status": "failure", "error": {"message": "invalid username or password"}}), 401

    @staticmethod
    def get_all_users():
        """
        Method for getting all users from data structures
        """
        Users.userLst.clear()
        if Database().get_all_users() is None:
            return jsonify({"status": "failure", "error": {"message": "no user found"}}), 404

        for user in Database().get_all_users():
            usr = {
                'user_id': user[0],
                'username': user[1],
                'firstname': user[2],
                'lastname': user[3],
                'contact': user[4],
                'email': user[5],
                'usertype': user[7]
            }
            Users.userLst.append(usr)
        return jsonify({"status": "success", "data": Users.userLst}), 200

    def check_user_details(self, username, email):
        """
        Method for checking users details
        """
        for user in Users.users:
            if user['username'] == username or user['email'] == email:
                return jsonify({"status": "failure", "error": {"message": "username or email already exists"}}), 403
        return False

    def get_user_id(self, username):
        """
        Method that return user_id
        """
        for user in Users.users:
            if user['username'] == username:
                return user['user_id']