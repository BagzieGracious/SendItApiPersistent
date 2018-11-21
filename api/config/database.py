import psycopg2


class Database:
    def __init__(self):
        try:
            self.connect = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                host='127.0.0.1',
                password='password'
            )
            self.cursor = self.connect.cursor()
            self.connect.autocommit = True

            tables = [
                """
                    CREATE TABLE IF NOT EXISTS users(
                        user_id SERIAL PRIMARY KEY, 
                        username VARCHAR(18) NOT NULL,
                        firstname VARCHAR(15) NOT NULL,
                        lastname VARCHAR(15) NOT NULL,
                        contact VARCHAR(15) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        password VARCHAR(200) NOT NULL,
                        usertype VARCHAR(8) NOT NULL
                    )
                """,

                """
                    CREATE TABLE IF NOT EXISTS orders(
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
            ]

            for table in tables:
                self.cursor.execute(table)

            sql = "SELECT * FROM users WHERE username = 'admin' "
            self.cursor.execute(sql)
            check = self.cursor.fetchone()
            if not check:
                admin = """
                            INSERT INTO users(username, firstname, lastname, contact, email, password, usertype) 
                            VALUES('admin', 'admin', 'admin', '0700500500', 'admin@sendit.com',
                            'sha256$7HCw6NOO$ca2881c0991da9973324e2b81d0b1e3cb6bfd890ff9a614f84dc3451d36e8284', 'admin')
                        """
                self.cursor.execute(admin)
        except:
            print("Cannot connect to database")

    def clear_tables(self):
        sql = "TRUNCATE TABLE users, orders RESTART IDENTITY"
        self.cursor.execute(sql)
        self.connect.commit()
