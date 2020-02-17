import environ


@environ.config(prefix="APP")
class AppConfig:
    @environ.config
    class Bot:
        token = environ.var()
        host = environ.var("0.0.0.0")
        port = environ.var(8000, converter=int)  
        webhook = environ.var() 

    @environ.config
    class Converter:
        fb2 = environ.var("FB2")
        cbz = environ.var("CBZ")
        pdf = environ.var("PDF") 

    debug = environ.var(False, converter=bool)
    db = environ.var()
    bot = environ.group(Bot)
    converter = environ.group(Converter)
