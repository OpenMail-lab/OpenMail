import json

LOG_FILE = "ip_log.json"

def update_ip(mac_address, new_ip):
    try:
        with open(LOG_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data[mac_address] = new_ip

    with open(LOG_FILE, "w") as file:
        json.dump(data, file)

def get_last_ip(mac_address):
    try:
        with open(LOG_FILE, "r") as file:
            data = json.load(file)
            return data.get(mac_address, "Unknown")
    except FileNotFoundError:
        return "Unknown"
