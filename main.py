import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

TESLA_URL = "https://www.tesla.com/tr_TR/inventory/api/v1/inventory-results"
PARAMS = {
    "query": {
        "model": "my",
        "arrangeby": "plh",
        "zip": "06420",
        "range": 0,
        "isVehicleVisible": True,
        "sort": "plh|desc"
    },
    "offset": 0,
    "count": 50,
    "outsideOffset": 0
}

LAST_VINS_FILE = "last_vins.json"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)


def load_last_vins():
    if os.path.exists(LAST_VINS_FILE):
        with open(LAST_VINS_FILE, "r") as f:
            return json.load(f)
    return []


def save_current_vins(vins):
    with open(LAST_VINS_FILE, "w") as f:
        json.dump(vins, f)


def fetch_current_vins():
    response = requests.post(TESLA_URL, json=PARAMS)
    data = response.json()
    return [vehicle["VIN"] for vehicle in data.get("results", [])]


def main():
    last_vins = load_last_vins()
    current_vins = fetch_current_vins()

    new_vins = [vin for vin in current_vins if vin not in last_vins]

    if new_vins:
        msg = f"🚗 Yeni {len(new_vins)} Tesla aracı bulundu:\n"
        msg += "\n".join(new_vins)
        send_telegram_message(msg)
        save_current_vins(current_vins)


if __name__ == "__main__":
    main()
