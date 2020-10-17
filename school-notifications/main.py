import json
import config
import schedule
import time
from datetime import date, timedelta, datetime
from utils import client, message_cache, homework_cache, save_messages, read_message, save_homework
from discord_webhook import DiscordWebhook

def log(message):
    ts = time.time()
    print("[" + datetime.fromtimestamp(ts).strftime('%H:%M %d/%m/%Y') + "]" + " " + message)

def send_webhook(content):
    webhook = DiscordWebhook(url=config.webhook_url, content=content)
    try:
        webhook.execute()
    except:
        log("Error while sending webhook occurred!")


def send_message(message):
    text = "<@%s>\n**Tytuł:** %s\n**Nadawca:** %s\n**Godzina:** %s\n**Treść:**```%s```" % (
        config.discord_user_id, message.title, message.sender.name, message.sent_time.strftime("%H:%M"), message.content
    )
    send_webhook(text)

def send_homework(homework):
    text = "<@%s>\n**Przedmiot:** %s\n**Termin:** %s\n**Treść:**```%s```" % (
        config.discord_user_id, homework.subject.name, homework.date.strftime("%d.%m.%Y"), homework.description
    )
    send_webhook(text)


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
            break
        else:
            message_cache.append(message.id)
            send_message(message)
            read_message(message.id)
            save_messages()

def check_homework():
    log("Checking homework...")
    for i in range(6): 
        homework = client.get_homework(date.today() + timedelta(days=i))
        homework_list = list(homework)
        for homework in homework_list: 
            if not homework: 
                homework_cache.append(homework.id)
                log("Invalid homework, skipping...")
                continue

            if homework.id in homework_cache:
                log("Homework found in cache, skipping...")
                continue
            else: 
                homework_cache.append(homework.id)
                send_homework(homework)
                save_homework()


log("Starting app...")
schedule.every(config.check_time).minutes.do(check_messages)
schedule.every(config.check_time).minutes.do(check_homework)
while 1:
    schedule.run_pending()
    time.sleep(1)
