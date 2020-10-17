from vulcan import Vulcan
import config
import json
from os import path

message_cache = []

if path.exists("./cert.json"):
    with open("./cert.json") as f:
        certificate = json.load(f)
        client = Vulcan(certificate)
else:
    certificate = Vulcan.register(config.credentials[0], config.credentials[1], config.credentials[2])
    client = Vulcan(certificate)
    with open("./cert.json", "w") as f:
        json.dump(certificate.json, f)

if path.exists("./messages.txt"):
    with open("./messages.txt") as f:
        message_cache = json.load(f)
else:
    message_cache = []
    with open("./messages.txt", "w") as f:
        json.dump(message_cache, f)