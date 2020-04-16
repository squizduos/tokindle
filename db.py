from mongoengine import *

import aiogram


class User(Document):
    tg_id = IntField(required=True)
    name = StringField(required=True)
    kindle = StringField()

    @classmethod
    async def get_or_create(cls, u: aiogram.types.User):
        obj = cls.objects(tg_id=u.id).first()
        if not obj:
            obj = cls(tg_id=u.id, name=u.full_name).save()
        return obj
