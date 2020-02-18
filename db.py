from mongoengine import *

class User(Document):
    name = StringField(required=True)
    tgid = IntField(required=True)
    kindle = ListField(StringField, max_length=4)