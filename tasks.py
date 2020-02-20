import asyncio

import requests
import os

import subprocess

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEImage import MIMEImage

import smtplib


def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

async def send_email(host, port, login, password, to, file_name):
    # create message object instance
    msg = MIMEMultipart()
    
    
    message = "Thank you"
    
    # setup the parameters of the message
    msg['From'] = login
    msg['To'] = to
    msg['Subject'] = file_name
    
    # add in the message body
    msg.attach(MIMEImage(open(file_name).read()))

    
    #create server
    server = smtplib.SMTP(f'{host}:{port}')
    
    server.starttls()
    
    # Login Credentials for sending the mail
    server.login(login, password)
    
    
    # send the message via the server.
    server.sendmail(login, to, msg.as_string())
    
    server.quit()


async def run_command(*args):
    """Run command in subprocess.

    Example from:
        http://asyncio.readthedocs.io/en/latest/subprocess.html
    """
    # Create subprocess
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    # Status
    print("Started: %s, pid=%s" % (args, process.pid), flush=True)

    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()

    # Progress
    if process.returncode == 0:
        print(
            "Done: %s, pid=%s, result: %s"
            % (args, process.pid, stdout.decode().strip()),
            flush=True,
        )
    else:
        print(
            "Failed: %s, pid=%s, result: %s"
            % (args, process.pid, stderr.decode().strip()),
            flush=True,
        )

    # Result
    result = stdout.decode().strip()

    # Return stdout
    return result


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop) 
    result = loop.run_until_complete(run_command("./bin/fb2c", "convert", "--to", "mobi", "/tmp/avidreaders.ru__vsya-stalnaya-krysa-tom-1.fb2.zip", "/tmp/"))
    print(result)
    loop.close()

main()