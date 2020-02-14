import argparse
import logging
import ssl
import sys


from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import *
from aiogram.utils.executor import start_polling, start_webhook

logging.basicConfig(level=logging.INFO)

async def cmd_start(message: types.Message):
    return SendMessage(message.chat.id, f"Hello, {message.from_user.full_name}!")
