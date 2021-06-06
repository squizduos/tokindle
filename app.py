import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import *
from aiogram.utils.executor import start_polling, start_webhook
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import set_webhook

from aiogram.utils.helper import Helper, HelperMode, ListItem

from bot import cmd_start, cmd_get_file, cmd_unable_to_process_file, cmd_register, UserState
from config import AppConfig

import environ

import mongoengine

logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher, url=None):
    dispatcher.middleware.setup(LoggingMiddleware())

    dispatcher.register_message_handler(cmd_start, state="*", commands=['start'])
    dispatcher.register_message_handler(cmd_register, state=[UserState.setup])
    dispatcher.register_message_handler(cmd_unable_to_process_file, content_types=types.ContentTypes.DOCUMENT,
                                        state=[UserState.setup, UserState.prepared, UserState.sent])
    dispatcher.register_message_handler(cmd_get_file, content_types=types.ContentTypes.DOCUMENT, state=UserState.ready)

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


async def on_shutdown(dispatcher: Dispatcher):
    logging.debug(f"Shutdowning...")
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def hello(request):
    return web.Response(text="Hello, world")


def main():
    cfg = environ.to_config(AppConfig)
    # Create bot & dispatcher instances.
    bot = Bot(token=cfg.bot.token, proxy=cfg.bot.proxy)
    storage = JSONStorage(os.path.join(cfg.temp_dir, "state.json"))
    dispatcher = Dispatcher(bot, storage=storage)

    mongoengine.disconnect()
    mongoengine.connect(host=cfg.db)

    if cfg.bot.host:
        webhook_path = f"/webhook/{cfg.bot.token}"
        executor = set_webhook(
            dispatcher=dispatcher,
            webhook_path=webhook_path,
            loop=None,
            skip_updates=None,
            on_startup=functools.partial(on_startup, url=f"https://{cfg.bot.host}{webhook_path}"),
            on_shutdown=on_shutdown,
            check_ip=False,
            retry_after=None,
            route_name='webhook_handler',
        )
        # Paste web here
        executor.web_app.add_routes([web.get('/', hello)])
        executor.run_app(host="0.0.0.0", port=cfg.bot.port, ssl_context=None)
    else:
        start_polling(dispatcher, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
