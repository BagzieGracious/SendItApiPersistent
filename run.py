"""
Main app root of the api endpoints
"""
from flask import Flask
from api.config import config
from api.config.routes import Routes
from api.config.database import Database


class Loader:
    """ 
    Create loader object to start server 
    """

    def __init__(self):
        self.route = Routes()
    
    def create_app(self, env_name):
        """
        static method for starting a server
        """
        # app initialization
        app = Flask(__name__)
        app.config.from_object(config.APP_CONFIG[env_name])

        # Directing to Routes
        self.route.fetch_routes(app)

        # Create database Tables
        Database().create_users_table()
        Database().create_order_table()

        return app


APP = Loader().create_app('development')

if __name__ == '__main__':
    APP.run(port=2000)
