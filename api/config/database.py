import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash


class Database:
    def __init__(self):
        try:
            self.con = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                host='127.0.0.1',
                password='password'
            )
            self.cur = self.con.cursor()
        except:
            print("Cannot connect to database")

    def create_users_table(self):
        tables = """CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY, 
                username VARCHAR(18) NOT NULL,
                firstname VARCHAR(15) NOT NULL,
                lastname VARCHAR(15) NOT NULL,
                contact VARCHAR(15) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(200) NOT NULL,
                usertype VARCHAR(8) NOT NULL
            )
        """
        self.cur.execute(tables)
        self.con.commit()

    def add_user(self, *args):
        pwd = generate_password_hash(args[5], method='sha256')
        sql = """INSERT INTO users(
            username, firstname, lastname, contact, email, password, usertype
        )VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        self.cur.execute(sql, (args[0], args[1], args[2], args[3], args[4], pwd, args[6]))
        self.con.commit()
        if self.check_user_exists(args[0], args[4]):
            return True
        return False

    def check_user_exists(self, username, email):
        sql = "SELECT * FROM users WHERE username='{}' OR email = '{}'".format(username, email)
        self.cur.execute(sql)
        if self.cur.fetchone():
            return True
        return False

    def authorize_user(self, username, password):
        sql = "SELECT * FROM users WHERE username='{}'".format(username)
        self.cur.execute(sql)
        data = self.cur.fetchone()
        if data is None:
            return False
        if check_password_hash(data[6], password):
            return True
        return False

    def user_data_username(self, username):
        sql = "SELECT * FROM users WHERE username='{}'".format(username)
        self.cur.execute(sql)
        return self.cur.fetchone()

    def get_all_users(self):
        sql = "SELECT * FROM users"
        self.cur.execute(sql)
        return self.cur.fetchall()

    def create_order_table(self):
        tables = """CREATE TABLE IF NOT EXISTS orders(
                order_id SERIAL PRIMARY KEY, 
                product VARCHAR(25) NOT NULL,
                description VARCHAR(100) NOT NULL,
                weight INT NOT NULL,
                order_status VARCHAR(15) NOT NULL,
                pickup VARCHAR(50) NOT NULL,
                destination VARCHAR(50) NOT NULL,
                user_id INT REFERENCES users(user_id),
                order_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.cur.execute(tables)
        self.con.commit()

    def add_parcel(self, order):
        sql = "SELECT * FROM orders WHERE user_id = %s AND product = %s AND destination = %s"
        self.cur.execute(sql, [order['user_id'], order['product'], order['destination']])

        if not self.cur.fetchone():
            sql1 = "INSERT INTO orders( product, description, weight, order_status, pickup, destination, user_id) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            self.cur.execute(sql1, [order['product'], order['description'], order['weight'], order['status'], order['pickup'], order['destination'], order['user_id']])
            self.con.commit()

            sql = "SELECT * FROM orders WHERE user_id = %s AND product = %s AND destination = %s"
            self.cur.execute(sql, [order['user_id'], order['product'], order['destination']])
            return self.cur.fetchone()
        return False

    def get_all_orders(self):
        sql = "SELECT * FROM orders"
        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_admin_single_order(self, order_id):
        sql = "SELECT * FROM orders WHERE order_id = %s"
        self.cur.execute(sql, [order_id])
        return self.cur.fetchone()

    def get_user_single_order(self, order_id, user_id):
        sql = "SELECT * FROM orders WHERE order_id = %s AND user_id = %s"
        self.cur.execute(sql, [order_id, user_id])
        return self.cur.fetchone()

    def get_order_by_user(self, user_id):
        sql = "SELECT * FROM orders WHERE user_id = %s"
        self.cur.execute(sql, [user_id])
        return self.cur.fetchall()

    def cancel_order(self, parcel_id):
        sql = "UPDATE orders SET order_status = 'cancelled' WHERE order_id = %s"
        self.cur.execute(sql, [parcel_id])
        self.con.commit()

        sql1 = "SELECT * FROM orders WHERE order_id = %s"
        self.cur.execute(sql1, [parcel_id])
        return self.cur.fetchone()

    def change_destination(self, parcel_id, destination):
        sql = "UPDATE orders SET destination = %s WHERE order_id = %s"
        self.cur.execute(sql, [destination, parcel_id])
        self.con.commit()

        sql1 = "SELECT * FROM orders WHERE order_id = %s"
        self.cur.execute(sql1, [parcel_id])
        return self.cur.fetchone()

    def change_status(self, parcel_id, status):
        sql = "UPDATE orders SET order_status = %s WHERE order_id = %s"
        self.cur.execute(sql, [status, parcel_id])
        self.con.commit()

        sql1 = "SELECT * FROM orders WHERE order_id = %s"
        self.cur.execute(sql1, [parcel_id])
        return self.cur.fetchone()

    def check_for_order_change(self, parcel_id):
        sql = "SELECT * FROM orders WHERE order_id = %s"
        self.cur.execute(sql, [parcel_id])
        return self.cur.fetchone()
