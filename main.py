from datetime import datetime, timedelta

import paramiko
import requests
import time

## Telegram bot settings
TOKEN = "aaa"
chat_id = "aaa"

## Server SSH settings to ping
host = "aaa"
username = "aaa"
password = "aaaa"
port = 22

# Uncomment this block to get chat id
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
# print(requests.get(url).json())

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
com = "uptime"

isLastSuccesfull = False

while True:
    try:
        client.connect(hostname=host, port=port, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(com)
        stdin.close()
        stdout = stdout.read()
        if not isLastSuccesfull:
            now = datetime.now()+ timedelta(hours=2)
            message = 'Питание восстановлено: ' + str(now.strftime("%d.%m.%Y %H:%M:%S"))
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
            requests.get(url)
        isLastSuccesfull = True
        client.close()

    except:
        if isLastSuccesfull:
            now = datetime.now()+ timedelta(hours=2)
            message = 'Питание потеряно: ' + str(now.strftime("%d.%m.%Y %H:%M:%S"))
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
            requests.get(url)
        isLastSuccesfull = False
    time.sleep(5)
