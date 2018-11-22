"""
Module for handling user business logic
"""
from werkzeug.security import check_password_hash, generate_password_hash
from api.config.database import Database


class Users:
    """
    User class that handles business logic for users
    """

    def __init__(self):
        self.connect = Database().connect
        self.cursor = Database().cursor

    def add_user(self, data):
        """
        Method for adding a user into a user table
        """
        pwd = generate_password_hash(data['password'], method='sha256')
        sql = """INSERT INTO users(username, firstname, lastname, contact, email, password, usertype)VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(sql, (data['username'], data['firstname'],data['lastname'], data['contact'], data['email'], pwd, data['usertype']))

    def check_credentials(self, username, password):
        """
        Method for checking users username and password
        """
        sql = "SELECT * FROM users WHERE username='{}'".format(username)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        if data is None:
            return False
        if check_password_hash(data['password'], password):
            return data
        return False

    def get_all_users(self):
        """
        Method for getting all users from the user table
        """
        sql = "SELECT * FROM users"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def check_user_details(self, username, email):
        """
        Method for checking users details
        """
        sql = "SELECT * FROM users WHERE username='{}' OR email = '{}'".format(username, email)
        self.cursor.execute(sql)
        if self.cursor.fetchone():
            return True
        return False

    def get_user_id(self, username):
        """
        Method that return user details
        """
        sql = "SELECT * FROM users WHERE username='{}'".format(username)
        self.cursor.execute(sql)
        return self.cursor.fetchone()
