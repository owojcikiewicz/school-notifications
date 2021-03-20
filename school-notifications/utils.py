import config
import json
from os import path
from vulcan import Keystore, Account, VulcanHebe, Vulcan

async def setup_client():
    if path.exists("./keystore.json"):
        with open("keystore.json") as f:
            keystore = Keystore.load(json.load(f))
    else: 
        with open("./keystore.json", "w") as f:
            keystore = Keystore.create(device_model="Vulcan API")
            json.dump(keystore.as_dict, f)

    if path.exists("./account.json"):
        with open("./account.json") as f:
            account = Account.load(json.load(f))
    else:
        account = await Account.register(keystore, config.credentials[0], config.credentials[1], config.credentials[2])
        with open("./account.json", "w") as f:
            json.dump(account.as_dict, f)

    if path.exists("./homework.txt"):
        with open("./homework.txt") as f:
            homework_cache = json.load(f)
    else:
        homework_cache = []
        with open("./homework.txt", "w") as f:
            json.dump(homework_cache, f)

    client = VulcanHebe(keystore, account)
    await client.select_student()

    return client, homework_cache

def save_homework(homework_cache): 
    with open("./homework.txt", "w") as fl: 
        json.dump(homework_cache, fl)