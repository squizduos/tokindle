import glob
import os
import asyncio
import logging

import requests

import config
import helpers

cfg = config.get()

logging.basicConfig(level=logging.INFO)


def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())


async def convert_fb2c(book_folder: str):
    program = os.path.join(os.curdir, cfg.converter.fb2)
    return_code, output = await helpers.run_command(program, "convert", "--to", "mobi", book_folder, book_folder)
    logging.info(f"Running FB2C for folder {book_folder}: return code {return_code}, output {output}")

    if return_code != 0:
        return None

    conv_search = glob.glob(os.path.join(book_folder, "*.mobi"))
    logging.info(f"MOBI files in folder {book_folder}: {conv_search}")
    if len(conv_search) > 0:
        return conv_search[0]
    # return return_code, output

async def upload_to_anonfile(upload_file):
    pass



def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop) 
    result = loop.run_until_complete(
        helpers.run_command("./bin/fb2c", "convert", "--to", "mobi", "/tmp/avidreaders.ru__vsya-stalnaya-krysa-tom-1.fb2.zip", "/tmp/"))
    print(result)
    loop.close()

# main()