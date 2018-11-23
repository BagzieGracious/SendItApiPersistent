"""
Module for configuring server environment variables
"""

class Security:
    def __init__(self):
        self.key = "EA92AB7D5FADB991CB064C72F65B1F13F011C2A5D7DCFD39"

class Config:
    """
    Default environment configuration
    """
    TESTING = False

class Development(Config):
    """
    Development environment configuration
    """
    DEBUG = True
    ENV = 'development'

class Production(Config):
    """
    Production environment configuration
    """
    DEBUG = False
    ENV = 'production'

APP_CONFIG = {
    'development': Development,
    'production': Production,
}
