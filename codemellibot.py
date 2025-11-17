import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "7452741:Xfzl_ojiKVoA7n5BlR3quePZNCasvlQIPYg"
SOURCE_USER_ID = 989991641701
TARGET_CHAT_ID = 9989387522360
API = f"https://tapi.bale.ai/bot{TOKEN}/"

@app.route("/", methods=["POST"])
def webhook():
    update = request.json
    if "message" in update:
        msg = update["message"]
        sender_id = msg["from"]["id"]

        if sender_id == SOURCE_USER_ID:
            message_id = msg["message_id"]

            requests.post(API + "forwardMessage", json={
                "chat_id": TARGET_CHAT_ID,
                "from_chat_id": sender_id,
                "message_id": message_id
            })
    return "OK"

if __name__ == "__main__":
    app.run(port=5000)


