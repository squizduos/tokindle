from os import environ


class Config:
    """Set configuration vars from .env file."""

    # General Config
    TOKEN = environ.get('TOKEN')

    HOST = environ.get('HOST')
    PORT = environ.get('PORT')

    WEBHOOK_HOST = environ.get('WEBHOOK_HOST')
    WEBHOOK_PORT = environ.get('WEBHOOK_PORT')
    WEBHOOK_PATH = environ.get('WEBHOOK_PATH')

    