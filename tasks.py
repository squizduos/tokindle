import glob
import os
import asyncio
import logging
import pathlib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import smtplib

import requests
import aiogram

import config
import db
import helpers

cfg = config.get()

logging.basicConfig(level=logging.INFO)


async def tg_download_file(document: aiogram.types.Document):
    url = await document.get_url()

    proxies = {}

    if cfg.bot.proxy:
        proxies.update(http=cfg.bot.proxy, https=cfg.bot.proxy)

    try:
        r = requests.get(url, proxies=proxies)
    except Exception as e:
        logging.error(f"Unable to download {url}: {str(e)}")
        return None

    if r.ok:
        download_path = os.path.join(cfg.temp_dir, document.file_unique_id)
        if not os.path.exists(download_path):
            os.mkdir(download_path)

        file_path = os.path.join(download_path, document.file_name)

        with open(file_path, 'wb') as f:
            f.write(r.content)

        return file_path
    else:
        logging.error(f"Unable to download {url}: status code {r.status_code}, result {r.text}")
        return None


async def convert_fb2c(book_file: str):
    conv_book_file = None
    book_folder = os.path.dirname(book_file)
    program, args = os.path.join(os.curdir, cfg.converter.fb2c), ["convert", "--to", "mobi", book_folder, book_folder]

    return_code, stdout, stderr = await helpers.run_command(program, *args)
    logging.debug(f"Running FB2C for folder {book_folder}: return code {return_code}, output")

    if return_code == 0:
        conv_search = glob.glob(os.path.join(book_folder, "*.mobi"))
        if len(conv_search) > 0:
            conv_book_file = conv_search[0]

    db.Convert(
        convert_id=os.path.basename(os.path.normpath(book_folder)),
        original_file=book_file,
        converted_file=conv_book_file,
        program=" ".join([program, *args]),
        return_code=return_code,
        stdout=stdout,
        stderr=stderr
    ).save()

    return conv_book_file


async def convert_kindlegen(book_file: str):
    conv_book_file = None
    book_folder = os.path.dirname(book_file)
    fname, _ = await helpers.get_file_name_extension(book_file)
    program, args = os.path.join(os.curdir, cfg.converter.kindlegen), [book_file, "-o", f"{fname}.mobi"]

    return_code, stdout, stderr = await helpers.run_command(program, *args)
    logging.debug(f"Running kindlegen for file {book_file}: return code {return_code}")

    # FIXME: kindlegen returns successful codes 0, 1.
    # More: https://www.mobileread.com/forums/showthread.php?t=269438
    if return_code in [0, 1]:
        conv_book_file = os.path.join(os.path.dirname(book_file), f"{fname}.mobi")

    db.Convert(
        convert_id=os.path.basename(os.path.normpath(book_folder)),
        original_file=book_file,
        converted_file=conv_book_file,
        program=" ".join([program, *args]),
        return_code=return_code,
        stdout=stdout,
        stderr=stderr
    ).save()

    return conv_book_file


async def send_email(to, file_name):
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    msg['From'] = cfg.email.username
    msg['To'] = to
    msg['Subject'] = file_name

    with open(file_name, 'rb') as f:
        fname = os.path.basename(file_name)
        attachment = MIMEApplication(
            f.read(),
            Content_Dispostition='attachment; filename=""%s"' % fname.split('.')[0],
            Name=fname
        )
        msg.attach(attachment)

    try:
        server = smtplib.SMTP_SSL(cfg.email.host, cfg.email.port, timeout=30)
        server.login(cfg.email.username, cfg.email.password)
        result = server.sendmail(cfg.email.username, to, msg.as_string())
    except Exception as e:
        logging.error(f"Unable to send {file_name} to {to}: {str(e)}")
        return None
    else:
        server.quit()
        return result