from aiogram.dispatcher.webhook import *

from db import User

logging.basicConfig(level=logging.INFO)


async def cmd_start(message: types.Message):
    user = User.objects(tgid=message.from_user.id)
    if not user:
        user = User(tgid=message.from_user.id, name=message.from_user.full_name).save()
    return SendMessage(message.chat.id, f"Hello, {message.from_user.full_name}!")
