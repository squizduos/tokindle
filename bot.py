import os
import time
import asyncio

from aiogram import Bot, types
from aiogram.dispatcher.webhook import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.bot.api import guess_filename

import config
from db import User
import helpers
import tasks

cfg = config.get()

logging.basicConfig(level=logging.INFO)


# States
class UserState(StatesGroup):
    setup = State()
    ready = State()
    prepared = State()
    sent = State()


async def cmd_start(message: types.Message, state: FSMContext):
    user = await User.get_or_create(message.from_user)
    if user.kindle:
        await UserState.ready.set()
        return SendMessage(
            message.chat.id,
            f"Здравствуйте, {user.name}! To Kindle - бот, который сконвертирует вашу книгу для Amazon Kindle.\n\n"
            f"Электронная почта вашего Kindle: **{user.kindle}**",
            parse_mode="Markdown"
        )
    else:
        await UserState.setup.set()
        return SendMessage(
            message.chat.id,
            f"Здравствуйте, {user.name}! To Kindle - бот, который сконвертирует вашу книгу для Amazon Kindle.\n\n"
            f"Чтобы начать, необходимо настроить доставку книг на ваш Kindle.\n"
            f"1. Перейдите по [ссылке](https://www.amazon.com/hz/mycd/myx#/home/settings/payment).\n"
            f"2. В разделе __Approved Personal Document E-mail List__ добавьте адрес **send@tokindle.ru**.\n"
            f"3. В разделе __Send-to-Kindle E-Mail Settings__ найдите почту своего Kindle и пришлите боту.\n",
            parse_mode="Markdown"
        )


async def cmd_register(message: types.Message, state: FSMContext):
    user = await User.get_or_create(message.from_user)

    email = message.text.strip()
    if email.endswith('@kindle.com') or email.endswith('@free.kindle.com'):
        user.kindle = email
        user.save()
        await UserState.ready.set()
        return SendMessage(
            message.chat.id,
            f"Регистрация успешно завершена. Бот готов к использованию.",
            parse_mode="Markdown"
        )
    else:
        return SendMessage(
            message.chat.id,
            f"Некорректный адрес электронной почты. Проверьте адрес и введите его снова.",
            parse_mode="Markdown"
        )


async def cmd_get_file(message: types.Message, state: FSMContext):
    bot = Bot.get_current()

    user = await User.get_or_create(message.from_user)

    await UserState.prepared.set()

    msg = await bot.send_message(
        message.chat.id,
        f"Запущен процесс конвертации для файла `{message.document.file_name}`",
        reply_to_message_id=message.message_id
    )

    await bot.edit_message_text(f"Скачиваем файл...", message.chat.id, msg.message_id, parse_mode="Markdown")

    book_file = await helpers.tg_download_file(message.document)

    if not book_file:
        await bot.edit_message_text(f"Ошибка скачивания файла.", message.chat.id, msg.message_id, parse_mode="Markdown")
        await UserState.ready.set()
        return msg

    await bot.edit_message_text(f"Конвертируем файл в MOBI...", message.chat.id, msg.message_id, parse_mode="Markdown")
    convert_book_file = await tasks.convert_fb2c(os.path.dirname(book_file))

    if not convert_book_file:
        await bot.edit_message_text(f"Ошибка конвертации файла.", message.chat.id, msg.message_id, parse_mode="Markdown")
        await UserState.ready.set()
        return msg

    await bot.edit_message_text(f"Отправляем файл по почте...", message.chat.id, msg.message_id, parse_mode="Markdown")
    send_result = await helpers.send_email(cfg.email.host, cfg.email.port, cfg.email.username, cfg.email.password, cfg.email.tls, user.kindle, convert_book_file)

    if send_result is None:
        await bot.edit_message_text(f"Ошибка отправки файла.", message.chat.id, msg.message_id, parse_mode="Markdown")
    else:
        await bot.edit_message_text(f"Файл успешно отправлен по электронному адресу {user.kindle}", message.chat.id, msg.message_id, parse_mode="Markdown")

    await UserState.ready.set()
    return msg


async def cmd_unable_to_process_file(message: types.Message, state: FSMContext):
    user = User.get_or_create(message.from_user)
    ping = datetime.datetime.now() - message.date
    await UserState.email.set()
    return SendMessage(message.chat.id, f"Невозможно!")
