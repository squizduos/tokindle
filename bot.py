import time
import asyncio

from aiogram import Bot, types
from aiogram.dispatcher.webhook import *
from aiogram.dispatcher import FSMContext
from aiogram.bot.api import guess_filename

from db import User

logging.basicConfig(level=logging.INFO)


async def cmd_start(message: types.Message):
    user = User.objects(tgid=message.from_user.id)
    if not user:
        user = User(tgid=message.from_user.id, name=message.from_user.full_name).save()
    return SendMessage(message.chat.id, f"Hello, {message.from_user.full_name}!")


async def cmd_get_file(message: types.Message, state: FSMContext):
    bot = Bot.get_current()
    url = await message.document.get_url()
    msg = await bot.send_message(message.chat.id, f"You send me file `{message.document.file_name}` via URL {url}", reply_to_message_id=message.message_id)
    await asyncio.sleep(5)
    msg = await bot.edit_message_text("Downloading message", message.chat.id, msg.message_id)
    await asyncio.sleep(5)
    msg = await bot.edit_message_text("Done", message.chat.id, msg.message_id)
    return msg