import asyncio

import requests
import os

import subprocess

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

async def launch(command):
    return os.popen(command).read()

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
    result = loop.run_until_complete(launch("./bin/fb2c convert --to mobi t.zip"))
    print(result)
    loop.close()

main()