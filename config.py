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
    class DB:
        host = environ.var()
        port = environ.var(27017, converter=int)
        username = environ.var()
        password = environ.var()
        name = environ.var()

    @environ.config
    class Converter:
        fb2 = environ.var("fb2c")
        mobi = environ.var("kindlegen")

    @environ.config
    class Email:
        host = environ.var()
        port = environ.var(465, converter=int)
        username = environ.var()
        password = environ.var()
        tls = environ.var(True, converter=bool)  
        address = environ.var()

    debug = environ.var(False, converter=bool)
    db = environ.group(DB)
    bot = environ.group(Bot)
    converter = environ.group(Converter)
