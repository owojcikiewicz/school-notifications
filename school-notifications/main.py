import json
import config
import time
from datetime import date, timedelta, datetime
from utils import setup_client, save_homework
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

def send_homework(homework):
    str_date = str(homework.deadline)
    date_raw = str_date.split()[0].split("-")
    date_parsed = date_raw[2] + "." + date_raw[1] + "." + date_raw[0]

    text = "@here\n**Przedmiot:** %s\n**Termin:** %s\n**Treść:**```%s```" % (
        homework.subject.name, date_parsed, homework.content
    )
    send_webhook(text)

async def check_homework(client, homework_cache):
    log("Checking homework...")

    homework_raw = await client.data.get_homework(date.today() - timedelta(days=1))
    async for homework in homework_raw: 
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
            save_homework(homework_cache)

async def main():
    global homework_cache 

    log("Starting app...")

    # Check Homework.
    for i in range(0, 100): 
        while True: 
            try: 
                client, homework_cache = await setup_client()
                await check_homework(client, homework_cache)
                await client.close()
                log("Stopping app...")
                return
            except: 
                log("Error occurred when checking homework, retrying...")
                continue 
            break 