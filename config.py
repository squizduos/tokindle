from os import environ

class Config:
    """Set configuration vars from .env file."""

    # General Config
    TOKEN = environ.get('TOKEN')
    SOCK = environ.get('SOCK')

    HOST = environ.get('HOST')
    PORT = environ.get('PORT')
    CERT = environ.get('CERT')
    PKEY = environ.get('PKEY')

    HOSTNAME = environ.get('HOSTNAME')
    WEBHOOK_PORT = environ.get('WEBHOOK_PORT')
    WEBHOOK_PATH = environ.get('WEBHOOK_PATH')
