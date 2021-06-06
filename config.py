import environ

import logging


@environ.config(prefix="APP")
class AppConfig:
    @environ.config
    class Bot:
        token = environ.var()
        proxy = environ.var()
        host = environ.var("0.0.0.0")
        port = environ.var(8080, converter=int)

    @environ.config
    class Converter:
        fb2c = environ.var()
        kindlegen = environ.var()

    @environ.config
    class Email:
        host = environ.var()
        port = environ.var(465, converter=int)
        username = environ.var()
        password = environ.var()
        tls = environ.var(True, converter=bool)  

    debug = environ.var(False, converter=bool)
    temp_dir = environ.var("/tmp/tokindle")
    db = environ.var()
    bot = environ.group(Bot)
    email = environ.group(Email)
    converter = environ.group(Converter)


def get_config():
    return environ.to_config(AppConfig)


def get_logger():
    cfg = get_config()
    logging_level = logging.DEBUG if cfg.debug else logging.INFO
    _logger = logging.getLogger('app')
    _logger.setLevel(logging_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    _logger.addHandler(ch)
    return _logger

