from aiogram.dispatcher.webhook import *

logging.basicConfig(level=logging.INFO)


async def cmd_start(message: types.Message):
    return SendMessage(message.chat.id, f"Hello, {message.from_user.full_name}!")
