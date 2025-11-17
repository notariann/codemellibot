import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://ble.ir/api/{BOT_TOKEN}"

DATA_FILE = "config.json"

def load_config():
    if not os.path.exists(DATA_FILE):
        return {"source_id": None, "target_id": None, "state": None}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

config = load_config()

def send_message(chat_id, text):
    requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

def forward(chat_id, from_chat_id, message_id):
    requests.post(
        f"{API_URL}/forwardMessage",
        json={
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id,
        },
    )

@app.route("/", methods=["POST"])
def webhook():
    update = request.json
    if not update:
        return "ok"

    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")
    from_user = message.get("from", {}).get("id")
    message_id = message.get("message_id")

    config = load_config()

    if text == "/setup":
        send_message(chat_id, "Enter SOURCE USER ID:")
        config["state"] = "WAIT_SOURCE"
        save_config(config)
        return "ok"

    if config.get("state") == "WAIT_SOURCE":
        if not text.isdigit():
            send_message(chat_id, "Invalid input.")
            return "ok"

        config["source_id"] = int(text)   # <-- YOU WILL ENTER THIS INSIDE THE CHAT
        config["state"] = "WAIT_TARGET"
        save_config(config)

        send_message(chat_id, "Enter TARGET CHAT ID:")
        return "ok"

    if config.get("state") == "WAIT_TARGET":
        if not text.isdigit():
            send_message(chat_id, "Invalid input.")
            return "ok"

        config["target_id"] = int(text)   # <-- YOU WILL ENTER THIS INSIDE THE CHAT
        config["state"] = "READY"
        save_config(config)

        send_message(chat_id, "Forwarding Active.")
        return "ok"

    if config.get("state") == "READY":
        if from_user == config.get("source_id"):
            forward(config.get("target_id"), chat_id, message_id)

    return "ok"

if name == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
