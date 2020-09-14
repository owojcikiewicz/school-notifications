from vulcan import Vulcan
from discord_webhook import DiscordWebhook
import config
import json
import schedule
import time
from os import path
import datetime

# Generate Certificate.
if path.exists("./cert.json"):
    with open("./cert.json") as f:
        certificate = json.load(f)
        client = Vulcan(certificate)
else:
    certificate = Vulcan.register(config.credentials[0], config.credentials[1], config.credentials[2])
    client = Vulcan(certificate)
    with open("./cert.json", "w") as f:
        json.dump(certificate.json, f)

# Retrieve Data.
if path.exists("./messages.txt"):
    with open("./messages.txt") as f:
        message_ids = json.load(f)
else:
    message_ids = []
    with open("./messages.txt", "w") as f:
        json.dump(message_ids, f)


# Basic Functions.
def save_messages():
    with open("./messages.txt", "w") as fl:
        json.dump(message_ids, fl)


def send_webhook(message):
    text = "<@%s>\n**Tytuł:** %s\n**Nadawca:** %s\n**Godzina:** %s\n**Treść:**```%s```" % (
        config.discord_user_id, message.title, message.sender.name, message.sent_time, message.content
    )
    webhook = DiscordWebhook(url=config.webhook_url, content=text)
    try:
        webhook.execute()
    except:
        print("Error while sending webhook occurred!")


def check_messages():
    messages_list = list(client.get_messages())
    for message in messages_list:
        if message.id in message_ids:
            continue
        else:
            message_ids.append(message.id)
            send_webhook(message)
            save_messages()


# Timers.
schedule.every(config.check_time).minutes.do(check_messages)
while 1:
    schedule.run_pending()
    time.sleep(1)
