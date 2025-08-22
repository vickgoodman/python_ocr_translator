import os
from dotenv import load_dotenv
import requests

def notify(msg):
    load_dotenv()

    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": os.getenv("PUSHOVER_API_TOKEN"),
        "user": os.getenv("PUSHOVER_USER_KEY"),
        "title": "Post Notifier",
        "message": msg,
    })
