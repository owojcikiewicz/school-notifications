import json
import config
import schedule
import time
import datetime
from cert import message_cache
from cert import client
from vulcan import Vulcan
from discord_webhook import DiscordWebhook

def log(message):
    ts = time.time()
    print("[" + datetime.datetime.fromtimestamp(ts).strftime('%H:%M %d/%m/%Y') + "]" + " " + message)


def save_messages():
    with open("./messages.txt", "w") as fl:
        json.dump(message_cache, fl)


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
    log("Checking messages...")
    messages_list = list(client.get_messages())
    for message in messages_list:
        if not message or not message.sender:
            message_cache.append(message.id)
            log("Invalid message, skipping...")
            continue

        if message.id in message_cache:
            log("Message found in cache, skipping...")
            continue
        else:
            message_cache.append(message.id)
            send_webhook(message)
            save_messages()


log("Starting app...")
schedule.every(config.check_time).minutes.do(check_messages)
while 1:
    schedule.run_pending()
    time.sleep(1)
