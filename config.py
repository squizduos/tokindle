import environ


@environ.config(prefix="APP")
class AppConfig:
    @environ.config
    class Bot:
        token = environ.var()
        proxy = environ.var()
        host = environ.var("0.0.0.0")
        port = environ.var(8000, converter=int)  
        webhook = environ.var()

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


def get():
    return environ.to_config(AppConfig)