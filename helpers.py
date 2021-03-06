import asyncio
import logging
import requests

import os

import subprocess

import config

import pathlib



import os
import random
import string


cfg = config.get_config()
logger = config.get_logger()


async def get_file_name_extension(book_file: str) -> (str, str):
    try:
        p = pathlib.Path(book_file)
        return p.stem, p.suffix
    except Exception as e:
        logger.error(e)
        return "", ""


def upload_file_to_url(upload_file, url):
    s = requests.Session()
    files = {'upload_file': open(upload_file, 'rb')}
    r = requests.Request('POST', url, files=files).prepare()
    resp = s.send(r)
    return resp.status_code


async def run_command(program, *args):
    """Run command in subprocess.

    Example from:
        http://asyncio.readthedocs.io/en/latest/subprocess.html
    """

    try:
        process = await asyncio.create_subprocess_exec(
            program, *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        logger.debug("Started: %s, pid=%s" % (args, process.pid))

        stdout, stderr = await process.communicate()
        stdout_s, stderr_s = stdout.decode().strip(), stderr.decode().strip()

        logger.debug(f"Done: {program} {' '.join(args)}\n")
        logger.debug(f"PID: {process.pid}\n")
        logger.debug(f"Return code: {process.returncode}\n")
        logger.debug(f"Stdout: {stdout_s}\n")
        logger.debug(f"Stderr: {stderr_s}\n")

        return process.returncode, stdout_s, stderr_s
    except Exception as e:
        logger.error(f"Failed: {program} {' '.join(args)}\n")
        logger.error(f"Exception: {str(e)}\n")
        return -1, "", ""
