import asyncio
import logging
import requests

import os

import subprocess

import config

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import smtplib

import aiogram

import os
import random
import string


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


def upload_file_to_url(upload_file, url):
    s = requests.Session()
    files = {'upload_file': open(upload_file, 'rb')}
    r = requests.Request('POST', url, files=files).prepare()
    resp = s.send(r)
    return resp.status_code


async def send_email(host, port, login, password, tls, to, file_name):
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    msg['From'] = login
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
        server = smtplib.SMTP_SSL(host, port, timeout=30)
        server.login(login, password)
        result = server.sendmail(login, to, msg.as_string())
    except Exception as e:
        logging.error(f"Unable to send {file_name} to {to}: {str(e)}")
        return None
    else:
        server.quit()
        return result


async def run_command(program, *args):
    """Run command in subprocess.

    Example from:
        http://asyncio.readthedocs.io/en/latest/subprocess.html
    """
    process = await asyncio.create_subprocess_exec(
        program, *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    print("Started: %s, pid=%s" % (args, process.pid), flush=True)

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        print(
            "Done: %s, pid=%s, result: %s"
            % (args, process.pid, stdout.decode().strip()),
            flush=True,
        )
        return process.returncode, stdout.decode().strip()
    else:
        print(
            "Failed: %s, pid=%s, result: %s"
            % (args, process.pid, stderr.decode().strip()),
            flush=True,
        )
        return process.returncode, stderr.decode().strip()
