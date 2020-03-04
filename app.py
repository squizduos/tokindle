import argparse
import logging
import ssl
import sys


from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import *
from aiogram.utils.executor import start_polling, start_webhook

import motor.motor_asyncio

from bot import cmd_start
from config import AppConfig

import environ

import mongoengine

logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher, url=None):
    dispatcher.register_message_handler(cmd_start, commands=['start', 'welcome'])

    bot = dispatcher.bot

    # Get current webhook status
    webhook = await bot.get_webhook_info()

    if url:
        # If URL is bad
        if webhook.url != url:
            # If URL doesnt match with by current remove webhook
            if not webhook.url:
                await bot.delete_webhook()
            await bot.set_webhook(url)
    elif webhook.url:
        # Otherwise remove webhook.
        await bot.delete_webhook()


async def on_shutdown(dispatcher):
    print('Shutdown.')


def main():
    cfg = environ.to_config(AppConfig)
    # Create bot & dispatcher instances.
    print(cfg)
    bot = Bot(token=cfg.bot.token, proxy=cfg.bot.proxy)
    dispatcher = Dispatcher(bot)

    mongoengine.disconnect()
    mongoengine.connect(host=cfg.db)

    if cfg.bot.webhook:
        path = f"/webhook/{cfg.bot.token}"
        url = f"https://{cfg.bot.webhook}{path}"
        start_webhook(dispatcher, path,
                      on_startup=functools.partial(on_startup, url=url),
                      on_shutdown=on_shutdown,
                      host=cfg.bot.host, port=cfg.bot.port, ssl_context=None)
    else:
        start_polling(dispatcher, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
