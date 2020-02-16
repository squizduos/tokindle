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
from config import Config

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
    # Create bot & dispatcher instances.
    bot = Bot(Config.TOKEN)
    dispatcher = Dispatcher(bot)

    if Config.HOST or Config.WEBHOOK_HOST:
        # Generate webhook URL
        webhook_url = f"https://{Config.WEBHOOK_HOST}:{Config.WEBHOOK_PORT}/{Config.WEBHOOK_PATH}"
        start_webhook(dispatcher, Config.WEBHOOK_PATH,
                      on_startup=functools.partial(on_startup, url=webhook_url),
                      on_shutdown=on_shutdown,
                      host=Config.HOST, port=Config.PORT, ssl_context=None)
    else:
        start_polling(dispatcher, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
