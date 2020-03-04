import requests

def upload_file_to_url(upload_file, url):
    s = requests.Session()
    files = {'upload_file': open(upload_file, 'rb')}
    r = requests.Request('POST', url, files=files).prepare()
    resp = s.send(r)
    return resp.status_code


async def send_email(host, port, login, password, to, file_name):
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    msg['From'] = login
    msg['To'] = to
    msg['Subject'] = file_name
    
    # add in the message body
    msg.attach(MIMEApplication(open(file_name).read()))
    
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