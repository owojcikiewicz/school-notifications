from vulcan import Vulcan
import config
import json
from os import path

# Generate Certificate.
if path.exists("./cert.json"):
    with open("./cert.json") as f:
        certificate = json.load(f)
else:
    certificate = Vulcan.register(config.credentials[0], config.credentials[1], config.credentials[2])
    with open("./cert.json", "w") as f:
        json.dump(certificate.json, f)

# Initialize Client.
client = Vulcan(certificate)


